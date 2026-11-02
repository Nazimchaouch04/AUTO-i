import React from 'react';
import { Shield, FileText, Scale } from 'lucide-react';

const LegalPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Mentions Légales
        </h1>

        <div className="space-y-8">
          {/* CGU */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <FileText className="w-6 h-6 text-blue-600 mr-3" />
              <h2 className="text-2xl font-semibold text-gray-800">
                Conditions Générales d'Utilisation (CGU)
              </h2>
            </div>
            <div className="prose prose-blue max-w-none text-gray-600">
              <h3 className="text-lg font-semibold text-gray-700 mt-4">1. Acceptation des CGU</h3>
              <p>
                En accédant et en utilisant la plateforme AutoIntel, vous acceptez les présentes Conditions Générales d'Utilisation. 
                Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser notre service.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">2. Description du Service</h3>
              <p>
                AutoIntel est une plateforme d'analyse du marché automobile qui fournit des estimations de prix, 
                des analyses de marché, et des services de mise en relation entre acheteurs et vendeurs de véhicules.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">3. Obligations de l'Utilisateur</h3>
              <ul className="list-disc pl-6 mt-2">
                <li>Fournir des informations exactes et à jour lors de l'inscription</li>
                <li>Ne pas utiliser la plateforme à des fins illégales ou frauduleuses</li>
                <li>Respecter les droits des autres utilisateurs</li>
                <li>Ne pas tenter de compromettre la sécurité du système</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">4. Compte Utilisateur</h3>
              <p>
                Vous êtes responsable de la confidentialité de vos identifiants de connexion. 
                Toute activité effectuée depuis votre compte est sous votre responsabilité.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">5. Contenu</h3>
              <p>
                Les utilisateurs sont seuls responsables du contenu qu'ils publient sur la plateforme. 
                AutoIntel se réserve le droit de modérer ou supprimer tout contenu inapproprié.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">6. Propriété Intellectuelle</h3>
              <p>
                Tous les éléments de la plateforme (design, code, textes, images, algorithmes) sont la propriété exclusive d'AutoIntel. 
                Toute reproduction sans autorisation est interdite.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">7. Limitation de Responsabilité</h3>
              <p>
                AutoIntel s'efforce de fournir des informations exactes mais ne garantit pas l'exactitude des estimations de prix. 
                La plateforme ne peut être tenue responsable des décisions prises sur la base de ces informations.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">8. Résiliation</h3>
              <p>
                AutoIntel se réserve le droit de suspendre ou résilier tout compte qui viole les présentes CGU.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">9. Modifications</h3>
              <p>
                AutoIntel se réserve le droit de modifier ces CGU à tout moment. 
                Les modifications seront notifiées aux utilisateurs par email.
              </p>
            </div>
          </div>

          {/* Privacy Policy */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Shield className="w-6 h-6 text-green-600 mr-3" />
              <h2 className="text-2xl font-semibold text-gray-800">
                Politique de Confidentialité
              </h2>
            </div>
            <div className="prose prose-green max-w-none text-gray-600">
              <h3 className="text-lg font-semibold text-gray-700 mt-4">1. Collecte des Données</h3>
              <p>
                Nous collectons les données suivantes:
              </p>
              <ul className="list-disc pl-6 mt-2">
                <li>Données d'inscription (nom, email, mot de passe haché)</li>
                <li>Données de profil (préférences, historique)</li>
                <li>Données d'utilisation (pages visitées, fonctionnalités utilisées)</li>
                <li>Données de paiement (traitées via Stripe, non stockées)</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">2. Utilisation des Données</h3>
              <p>
                Vos données sont utilisées pour:
              </p>
              <ul className="list-disc pl-6 mt-2">
                <li>Fournir et améliorer nos services</li>
                <li>Personnaliser votre expérience</li>
                <li>Envoyer des notifications (avec votre consentement)</li>
                <li>Assurer la sécurité de la plateforme</li>
                <li>Respecter nos obligations légales</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">3. Partage des Données</h3>
              <p>
                Nous ne partageons vos données personnelles avec des tiers que dans les cas suivants:
              </p>
              <ul className="list-disc pl-6 mt-2">
                <li>Avec votre consentement explicite</li>
                <li>Avec nos prestataires de services (Stripe, hébergement)</li>
                <li>Si requis par la loi</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">4. Sécurité des Données</h3>
              <p>
                Nous mettons en œuvre des mesures de sécurité appropriées pour protéger vos données:
              </p>
              <ul className="list-disc pl-6 mt-2">
                <li>Cryptage des données sensibles</li>
                <li>Authentification sécurisée (JWT)</li>
                <li>Accès restreint aux données</li>
                <li>Tests de sécurité réguliers</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">5. Vos Droits (RGPD)</h3>
              <p>
                Conformément au RGPD, vous avez les droits suivants:
              </p>
              <ul className="list-disc pl-6 mt-2">
                <li>Droit d'accès à vos données</li>
                <li>Droit de rectification</li>
                <li>Droit à l'effacement</li>
                <li>Droit à la portabilité</li>
                <li>Droit d'opposition</li>
                <li>Droit de retirer votre consentement</li>
              </ul>
              <p className="mt-2">
                Pour exercer ces droits, contactez-nous à: privacy@autointel.com
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">6. Conservation des Données</h3>
              <p>
                Vos données sont conservées tant que votre compte est actif. 
                Après suppression, elles sont conservées pendant la durée légale requise.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">7. Cookies</h3>
              <p>
                Nous utilisons des cookies pour améliorer votre expérience. 
                Vous pouvez gérer vos préférences de cookies dans les paramètres de votre navigateur.
              </p>
            </div>
          </div>

          {/* Terms of Service */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Scale className="w-6 h-6 text-purple-600 mr-3" />
              <h2 className="text-2xl font-semibold text-gray-800">
                Conditions de Service
              </h2>
            </div>
            <div className="prose prose-purple max-w-none text-gray-600">
              <h3 className="text-lg font-semibold text-gray-700 mt-4">1. Abonnements et Paiements</h3>
              <p>
                Les abonnements sont facturés mensuellement ou annuellement selon le plan choisi. 
                Les paiements sont sécurisés via Stripe.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">2. Remboursements</h3>
              <p>
                Les remboursements peuvent être demandés dans les 14 jours suivant l'achat, 
                sous condition de non-utilisation des services payants.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">3. Annulation</h3>
              <p>
                Vous pouvez annuler votre abonnement à tout moment depuis votre compte. 
                L'accès aux services payants reste actif jusqu'à la fin de la période facturée.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">4. Disponibilité du Service</h3>
              <p>
                Nous nous efforçons de maintenir une disponibilité de 99.9%. 
                Des interruptions peuvent survenir pour maintenance ou mises à jour.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">5. Support Client</h3>
              <p>
                Notre support est disponible par email à support@autointel.com 
                avec un temps de réponse garanti sous 24h ouvrées.
              </p>

              <h3 className="text-lg font-semibold text-gray-700 mt-4">6. Loi Applicable</h3>
              <p>
                Les présentes conditions sont régies par le droit français. 
                Tout litige sera soumis aux tribunaux compétents en France.
              </p>
            </div>
          </div>

          {/* Contact */}
          <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
            <h3 className="text-xl font-semibold text-blue-900 mb-3">Contact</h3>
            <p className="text-blue-800">
              Pour toute question concernant ces mentions légales, contactez-nous à:
            </p>
            <p className="text-blue-800 font-medium mt-2">
              legal@autointel.com
            </p>
            <p className="text-blue-600 text-sm mt-2">
              Dernière mise à jour: Janvier 2024
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LegalPage;
