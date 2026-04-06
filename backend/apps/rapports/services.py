import os
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from .models import RapportPDF, TemplateRapport, HistoriqueGeneration
import logging

logger = logging.getLogger(__name__)

class RapportPDFService:
    """Service pour la génération de rapports PDF"""
    
    def __init__(self):
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'rapports', 'pdf')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def creer_rapport(self, user, type_rapport, titre, **kwargs):
        """Crée un nouveau rapport PDF"""
        try:
            rapport = RapportPDF.objects.create(
                user=user,
                type_rapport=type_rapport,
                titre=titre,
                **kwargs
            )
            
            # Définit la date d'expiration (30 jours)
            rapport.expire_at = timezone.now() + timedelta(days=30)
            rapport.save()
            
            logger.info(f"Rapport créé: {rapport.id} - {titre}")
            return rapport
            
        except Exception as e:
            logger.error(f"Erreur création rapport: {e}")
            raise
    
    def generer_donnees_rapport(self, rapport):
        """Génère les données structurées pour le rapport"""
        try:
            if rapport.type_rapport == 'complet':
                return self._generer_donnees_rapport_complet(rapport)
            elif rapport.type_rapport == 'comparatif':
                return self._generer_donnees_rapport_comparatif(rapport)
            elif rapport.type_rapport == 'historique':
                return self._generer_donnees_rapport_historique(rapport)
            elif rapport.type_rapport == 'estimation':
                return self._generer_donnees_rapport_estimation(rapport)
            else:
                raise ValueError(f"Type de rapport non supporté: {rapport.type_rapport}")
                
        except Exception as e:
            logger.error(f"Erreur génération données rapport {rapport.id}: {e}")
            raise
    
    def _generer_donnees_rapport_complet(self, rapport):
        """Génère les données pour un rapport complet"""
        annonce = rapport.annonce_principale
        if not annonce:
            raise ValueError("Annonce principale requise pour rapport complet")
        
        # Récupère les annonces similaires pour comparaison
        from apps.annonces.models import Annonce
        similaires = Annonce.objects.filter(
            vehicule__marque=annonce.vehicule.marque,
            vehicule__modele=annonce.vehicule.modele,
            annee__range=(annonce.annee - 2, annonce.annee + 2),
            est_active=True
        ).exclude(id=annonce.id)[:10]
        
        # Statistiques du marché
        prix_moyen = similaires.aggregate(prix_moyen=models.Avg('prix'))['prix_moyen'] or 0
        prix_min = similaires.aggregate(prix_min=models.Min('prix'))['prix_min'] or 0
        prix_max = similaires.aggregate(prix_max=models.Max('prix'))['prix_max'] or 0
        
        return {
            'annonce': {
                'id': annonce.id,
                'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele} {annonce.annee}",
                'prix': annonce.prix,
                'kilometrage': annonce.kilometrage,
                'annee': annonce.annee,
                'carburant': annonce.carburant,
                'boite': annonce.boite,
                'ville': annonce.ville,
                'pays': annonce.pays,
                'date_collecte': annonce.date_collecte,
                'url': f"https://autointel.dz/annonces/{annonce.id}",
                'prix_estime': annonce.prix_estime,
                'ecart_prix': annonce.ecart_prix,
                'description': annonce.description or '',
                'equipements': annonce.equipements or [],
            },
            'analyse_marche': {
                'prix_moyen': prix_moyen,
                'prix_min': prix_min,
                'prix_max': prix_max,
                'nb_annonces': similaires.count(),
                'position_marche': self._calculer_position_marche(annonce.prix, prix_min, prix_max),
            },
            'similaires': [
                {
                    'id': a.id,
                    'titre': f"{a.vehicule.marque} {a.vehicule.modele} {a.annee}",
                    'prix': a.prix,
                    'kilometrage': a.kilometrage,
                    'annee': a.annee,
                    'ville': a.ville,
                    'url': f"https://autointel.dz/annonces/{a.id}",
                } for a in similaires
            ],
            'conseils': self._generer_conseils(annonce, prix_moyen),
            'date_generation': timezone.now(),
        }
    
    def _generer_donnees_rapport_comparatif(self, rapport):
        """Génère les données pour un rapport comparatif"""
        annonces = list(rapport.annonces_comparees.all())
        if len(annonces) < 2:
            raise ValueError("Au moins 2 annonces requises pour rapport comparatif")
        
        # Analyse comparative
        prix_moyen = sum(a.prix for a in annonces) / len(annonces)
        km_moyen = sum(a.kilometrage for a in annonces) / len(annonces)
        
        return {
            'annonces': [
                {
                    'id': a.id,
                    'titre': f"{a.vehicule.marque} {a.vehicule.modele} {a.annee}",
                    'prix': a.prix,
                    'kilometrage': a.kilometrage,
                    'annee': a.annee,
                    'carburant': a.carburant,
                    'boite': a.boite,
                    'ville': a.ville,
                    'prix_estime': a.prix_estime,
                    'ecart_prix': a.ecart_prix,
                    'url': f"https://autointel.dz/annonces/{a.id}",
                } for a in annonces
            ],
            'analyse': {
                'prix_moyen': prix_moyen,
                'km_moyen': km_moyen,
                'meilleur_prix': min(a.prix for a in annonces),
                'meilleur_km': min(a.kilometrage for a in annonces),
                'recommandation': self._determiner_meilleur_choix(annonces),
            },
            'date_generation': timezone.now(),
        }
    
    def _generer_donnees_rapport_historique(self, rapport):
        """Génère les données pour un rapport historique"""
        alerte = rapport.alerte_source
        if not alerte:
            raise ValueError("Alerte source requise pour rapport historique")
        
        # Récupère les résultats de l'alerte
        from apps.alertes.models import ResultatAlerte
        resultats = ResultatAlerte.objects.filter(alerte=alerte).select_related('annonce').order_by('-created_at')
        
        # Évolution des prix
        annonces = [r.annonce for r in resultats if r.annonce]
        prix_par_mois = {}
        
        for annonce in annonces:
            mois_key = annonce.date_collecte.strftime('%Y-%m')
            if mois_key not in prix_par_mois:
                prix_par_mois[mois_key] = []
            prix_par_mois[mois_key].append(annonce.prix)
        
        evolution = {
            mois: {
                'prix_moyen': sum(prix) / len(prix),
                'prix_min': min(prix),
                'prix_max': max(prix),
                'nb_annonces': len(prix),
            } for mois, prix in prix_par_mois.items()
        }
        
        return {
            'alerte': {
                'id': alerte.id,
                'nom': alerte.nom,
                'critere': {
                    'marque': alerte.marque,
                    'modele': alerte.modele,
                    'prix_max': alerte.prix_max,
                    'km_max': alerte.km_max,
                }
            },
            'evolution_prix': evolution,
            'statistiques': {
                'total_annonces': len(annonces),
                'prix_actuel_moyen': prix_par_mois.get(list(prix_par_mois.keys())[-1], {}).get('prix_moyen', 0) if prix_par_mois else 0,
                'tendance': self._calculer_tendance(evolution),
            },
            'recentes': [
                {
                    'id': a.id,
                    'titre': f"{a.vehicule.marque} {a.vehicule.modele} {a.annee}",
                    'prix': a.prix,
                    'date': a.date_collecte,
                    'url': f"https://autointel.dz/annonces/{a.id}",
                } for a in annonces[:10]
            ],
            'date_generation': timezone.now(),
        }
    
    def _generer_donnees_rapport_estimation(self, rapport):
        """Génère les données pour un rapport d'estimation"""
        annonce = rapport.annonce_principale
        if not annonce:
            raise ValueError("Annonce principale requise pour rapport d'estimation")
        
        # Analyse détaillée pour l'estimation
        return {
            'annonce': {
                'id': annonce.id,
                'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele} {annonce.annee}",
                'prix': annonce.prix,
                'kilometrage': annonce.kilometrage,
                'annee': annonce.annee,
                'carburant': annonce.carburant,
                'boite': annonce.boite,
            },
            'estimation': {
                'prix_estime': annonce.prix_estime,
                'ecart_prix': annonce.ecart_prix,
                'confiance': self._calculer_confiance_estimation(annonce),
                'facteurs': self._analyser_facteurs_estimation(annonce),
            },
            'marche': self._analyser_marche_local(annonce),
            'recommandations': self._generer_recommandations_estimation(annonce),
            'date_generation': timezone.now(),
        }
    
    def generer_pdf(self, rapport):
        """Génère le fichier PDF à partir des données du rapport"""
        try:
            debut = timezone.now()
            
            # Enregistre le début de génération
            HistoriqueGeneration.objects.create(
                rapport=rapport,
                action='generation',
                statut='en_cours',
                message='Début de la génération PDF'
            )
            
            # Génère les données
            donnees = self.generer_donnees_rapport(rapport)
            rapport.contenu_json = donnees
            rapport.save()
            
            # Nom du fichier
            filename = f"rapport_{rapport.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Crée le PDF avec ReportLab
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#2563eb'),
                alignment=1  # Centre
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.HexColor('#1e40af'),
            )
            
            # En-tête
            story.append(Paragraph(f"RAPPORT {rapport.get_type_rapport_display().upper()}", title_style))
            story.append(Paragraph(f"{rapport.titre}", styles['Heading2']))
            story.append(Spacer(1, 20))
            
            # Contenu spécifique selon le type
            if rapport.type_rapport == 'complet':
                story.extend(self._generer_contenu_rapport_complet(donnees, styles))
            elif rapport.type_rapport == 'comparatif':
                story.extend(self._generer_contenu_rapport_comparatif(donnees, styles))
            elif rapport.type_rapport == 'historique':
                story.extend(self._generer_contenu_rapport_historique(donnees, styles))
            elif rapport.type_rapport == 'estimation':
                story.extend(self._generer_contenu_rapport_estimation(donnees, styles))
            
            # Pied de page
            story.append(PageBreak())
            story.append(Paragraph("Généré par AutoIntel", styles['Normal']))
            story.append(Paragraph(f"Date: {timezone.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            
            # Génère le PDF
            doc.build(story)
            
            # Sauvegarde le fichier dans le modèle
            with open(filepath, 'rb') as f:
                rapport.fichier_pdf.save(filename, ContentFile(f.read()))
            
            # Met à jour le statut
            rapport.statut_paiement = 'termine'
            rapport.genere_at = timezone.now()
            rapport.save()
            
            # Enregistre le succès
            temps_execution = timezone.now() - debut
            HistoriqueGeneration.objects.create(
                rapport=rapport,
                action='generation',
                statut='succes',
                message='PDF généré avec succès',
                temps_execution=temps_execution
            )
            
            # Nettoie le fichier temporaire
            os.remove(filepath)
            
            logger.info(f"PDF généré avec succès: {rapport.id}")
            return True
            
        except Exception as e:
            # Enregistre l'erreur
            HistoriqueGeneration.objects.create(
                rapport=rapport,
                action='generation',
                statut='erreur',
                message=str(e)
            )
            
            logger.error(f"Erreur génération PDF {rapport.id}: {e}")
            rapport.statut_paiement = 'erreur'
            rapport.save()
            raise
    
    def _get_template(self, type_rapport):
        """Retourne le nom du template pour le type de rapport"""
        templates = {
            'complet': 'rapport_complet',
            'comparatif': 'rapport_comparatif',
            'historique': 'rapport_historique',
            'estimation': 'rapport_estimation',
        }
        return templates.get(type_rapport, 'rapport_complet')
    
    def _get_css_styles(self):
        """Retourne les styles CSS pour le PDF"""
        return """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 12px;
            line-height: 1.6;
            color: #333;
        }
        
        .header {
            text-align: center;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #2563eb;
            font-size: 28px;
            margin: 0;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section h2 {
            color: #1e40af;
            font-size: 20px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        .table th,
        .table td {
            border: 1px solid #e5e7eb;
            padding: 10px;
            text-align: left;
        }
        
        .table th {
            background-color: #f3f4f6;
            font-weight: bold;
        }
        
        .highlight {
            background-color: #fef3c7;
            padding: 15px;
            border-left: 4px solid #f59e0b;
            margin-bottom: 20px;
        }
        
        .price {
            font-size: 18px;
            font-weight: bold;
            color: #059669;
        }
        
        .price-high {
            color: #dc2626;
        }
        
        .price-low {
            color: #059669;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            font-size: 10px;
            color: #6b7280;
        }
        """
    
    # Méthodes pour générer le contenu PDF avec ReportLab
    def _generer_contenu_rapport_complet(self, donnees, styles):
        """Génère le contenu pour un rapport complet"""
        story = []
        
        # Informations sur l'annonce
        annonce = donnees['annonce']
        story.append(Paragraph("DÉTAILS DE L'ANNONCE", styles['Heading2']))
        
        data = [
            ['Véhicule', annonce['titre']],
            ['Prix', f"{annonce['prix']:,.0f} €"],
            ['Kilométrage', f"{annonce['kilometrage']:,} km"],
            ['Année', str(annonce['annee'])],
            ['Carburant', annonce['carburant']],
            ['Boîte', annonce['boite']],
            ['Localisation', f"{annonce['ville']}, {annonce['pays']}"],
        ]
        
        if annonce['prix_estime']:
            data.append(['Prix Estimé', f"{annonce['prix_estime']:,.0f} €"])
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Analyse du marché
        analyse = donnees['analyse_marche']
        story.append(Paragraph("ANALYSE DU MARCHÉ", styles['Heading2']))
        
        marche_data = [
            ['Prix Moyen', f"{analyse['prix_moyen']:,.0f} €"],
            ['Prix Minimum', f"{analyse['prix_min']:,.0f} €"],
            ['Prix Maximum', f"{analyse['prix_max']:,.0f} €"],
            ['Nombre d\'annonces', str(analyse['nb_annonces'])],
            ['Position sur le marché', f"{analyse['position_marche']:.1f}%"],
        ]
        
        marche_table = Table(marche_data, colWidths=[2*inch, 2*inch])
        marche_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(marche_table)
        story.append(Spacer(1, 20))
        
        # Conseils
        if donnees['conseils']:
            story.append(Paragraph("CONSEILS", styles['Heading2']))
            for conseil in donnees['conseils']:
                story.append(Paragraph(f"• {conseil}", styles['Normal']))
            story.append(Spacer(1, 12))
        
        return story
    
    def _generer_contenu_rapport_comparatif(self, donnees, styles):
        """Génère le contenu pour un rapport comparatif"""
        story = []
        
        # Tableau comparatif
        story.append(Paragraph("COMPARAISON DES ANNONCES", styles['Heading2']))
        
        headers = ['Véhicule', 'Prix', 'Kilométrage', 'Année']
        data = [headers]
        
        for annonce in donnees['annonces']:
            data.append([
                annonce['titre'],
                f"{annonce['prix']:,.0f} €",
                f"{annonce['kilometrage']:,} km",
                str(annonce['annee'])
            ])
        
        table = Table(data, colWidths=[3*inch, 1.2*inch, 1.2*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Analyse
        analyse = donnees['analyse']
        story.append(Paragraph("ANALYSE COMPARATIVE", styles['Heading2']))
        
        analyse_data = [
            ['Prix Moyen', f"{analyse['prix_moyen']:,.0f} €"],
            ['Kilométrage Moyen', f"{analyse['km_moyen']:,.0f} km"],
            ['Meilleur Prix', f"{analyse['meilleur_prix']:,.0f} €"],
            ['Meilleur Kilométrage', f"{analyse['meilleur_km']:,} km"],
        ]
        
        analyse_table = Table(analyse_data, colWidths=[2.5*inch, 1.5*inch])
        analyse_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(analyse_table)
        
        return story
    
    def _generer_contenu_rapport_historique(self, donnees, styles):
        """Génère le contenu pour un rapport historique"""
        story = []
        
        # Informations sur l'alerte
        alerte = donnees['alerte']
        story.append(Paragraph("PARAMÈTRES DE L'ALERTE", styles['Heading2']))
        
        alerte_data = [
            ['Nom', alerte['nom']],
            ['Marque', alerte['critere']['marque'] or 'Toutes'],
            ['Modèle', alerte['critere']['modele'] or 'Tous'],
            ['Prix Maximum', f"{alerte['critere']['prix_max']:,.0f} €" if alerte['critere']['prix_max'] else 'Non défini'],
            ['Kilométrage Maximum', f"{alerte['critere']['km_max']:,} km" if alerte['critere']['km_max'] else 'Non défini'],
        ]
        
        alerte_table = Table(alerte_data, colWidths=[2*inch, 3*inch])
        alerte_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(alerte_table)
        story.append(Spacer(1, 20))
        
        # Statistiques
        stats = donnees['statistiques']
        story.append(Paragraph("STATISTIQUES", styles['Heading2']))
        
        stats_data = [
            ['Total Annonces', str(stats['total_annonces'])],
            ['Prix Actuel Moyen', f"{stats['prix_actuel_moyen']:,.0f} €"],
            ['Tendance', stats['tendance']],
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        
        return story
    
    def _generer_contenu_rapport_estimation(self, donnees, styles):
        """Génère le contenu pour un rapport d'estimation"""
        story = []
        
        # Détails du véhicule
        annonce = donnees['annonce']
        story.append(Paragraph("CARACTÉRISTIQUES", styles['Heading2']))
        
        vehicule_data = [
            ['Véhicule', annonce['titre']],
            ['Prix Actuel', f"{annonce['prix']:,.0f} €"],
            ['Kilométrage', f"{annonce['kilometrage']:,} km"],
            ['Année', str(annonce['annee'])],
            ['Carburant', annonce['carburant']],
            ['Boîte', annonce['boite']],
        ]
        
        vehicule_table = Table(vehicule_data, colWidths=[2*inch, 3*inch])
        vehicule_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(vehicule_table)
        story.append(Spacer(1, 20))
        
        # Estimation
        estimation = donnees['estimation']
        story.append(Paragraph("ESTIMATION AUTOINTEL", styles['Heading2']))
        
        estimation_data = [
            ['Prix Estimé', f"{estimation['prix_estime']:,.0f} €"],
            ['Écart Prix', f"{estimation['ecart_prix']:+.1f}%"],
            ['Niveau de Confiance', f"{estimation['confiance']:.0f}%"],
        ]
        
        estimation_table = Table(estimation_data, colWidths=[2*inch, 2*inch])
        estimation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(estimation_table)
        story.append(Spacer(1, 20))
        
        # Facteurs d'influence
        if estimation['facteurs']:
            story.append(Paragraph("FACTEURS D'INFLUENCE", styles['Heading2']))
            for facteur in estimation['facteurs']:
                story.append(Paragraph(f"• {facteur}", styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Recommandations
        if donnees['recommandations']:
            story.append(Paragraph("RECOMMANDATIONS", styles['Heading2']))
            for reco in donnees['recommandations']:
                story.append(Paragraph(f"• {reco}", styles['Normal']))
        
        return story
    
    # Méthodes utilitaires
