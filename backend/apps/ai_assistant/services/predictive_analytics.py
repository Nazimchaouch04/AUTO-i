"""
Predictive analytics helpers for the AI assistant.
"""

from __future__ import annotations

import calendar
from datetime import datetime
from statistics import mean, pstdev
from typing import Any, Dict, List, Optional, Tuple

from django.db.models import Avg, Count, Max, Min, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.annonces.models import Annonce

from ..models import UserProfileAnalysis


class PredictiveAnalyticsService:
    """Builds market projections from annonce data."""

    def __init__(self, user=None):
        self.user = user

    def build_predictive_report(
        self,
        filters: Optional[Dict[str, Any]] = None,
        external_context: Optional[Dict[str, Any]] = None,
        forecast_months: int = 6,
        lookback_months: int = 12,
    ) -> Dict[str, Any]:
        filters = self._clean_filters(filters)
        filters, personalization_notes = self._apply_profile_defaults(filters)

        queryset = self._build_queryset(filters)
        market_snapshot = self._build_market_snapshot(
            queryset=queryset,
            lookback_months=lookback_months,
        )

        event_impact = self.evaluate_external_impacts(
            filters=filters,
            external_context=external_context,
        )

        price_forecast = self.predict_market_prices(
            filters=filters,
            forecast_months=forecast_months,
            queryset=queryset,
            market_snapshot=market_snapshot,
            event_impact=event_impact,
        )

        best_periods = self.identify_best_periods(
            market_snapshot=market_snapshot,
            price_forecast=price_forecast,
        )

        market_insights = self.generate_market_insights(
            filters=filters,
            market_snapshot=market_snapshot,
            price_forecast=price_forecast,
            event_impact=event_impact,
            best_periods=best_periods,
        )

        custom_trends = self._build_custom_trends(
            filters=filters,
            market_snapshot=market_snapshot,
            price_forecast=price_forecast,
            best_periods=best_periods,
            personalization_notes=personalization_notes,
        )

        return {
            "generated_at": timezone.now(),
            "scope": {
                "filters": filters,
                "matching_annonces": market_snapshot["matching_annonces"],
                "lookback_months": lookback_months,
                "forecast_months": forecast_months,
            },
            "current_market": {
                "average_price": market_snapshot["current_average_price"],
                "median_proxy_price": market_snapshot["median_proxy_price"],
                "min_price": market_snapshot["price_range"]["min"],
                "max_price": market_snapshot["price_range"]["max"],
                "good_deal_ratio": market_snapshot["good_deal_ratio"],
                "listing_count": market_snapshot["matching_annonces"],
                "top_brands": market_snapshot["top_brands"],
                "fuel_mix": market_snapshot["fuel_mix"],
            },
            "price_forecast": price_forecast,
            "best_periods": best_periods,
            "event_impact": event_impact,
            "market_insights": market_insights,
            "custom_trends": custom_trends,
            "data_quality": {
                "historical_points": len(market_snapshot["historical_series"]),
                "confidence": price_forecast["confidence"],
                "has_external_context": bool(
                    self._normalize_external_context(external_context)
                ),
            },
        }

    def predict_market_prices(
        self,
        filters: Optional[Dict[str, Any]] = None,
        forecast_months: int = 6,
        queryset=None,
        market_snapshot: Optional[Dict[str, Any]] = None,
        event_impact: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        filters = self._clean_filters(filters)
        queryset = queryset or self._build_queryset(filters)
        market_snapshot = market_snapshot or self._build_market_snapshot(queryset, 12)
        event_impact = event_impact or self.evaluate_external_impacts(filters=filters)

        historical_series = market_snapshot["historical_series"]
        current_average = market_snapshot["current_average_price"]

        if not historical_series and current_average <= 0:
            return {
                "summary": "Pas assez de donnees pour produire une projection fiable.",
                "current_average_price": 0.0,
                "forecast_horizon_months": forecast_months,
                "trend_direction": "stable",
                "trend_strength_pct": 0.0,
                "monthly_trend_pct": 0.0,
                "volatility_pct": 0.0,
                "confidence": 20,
                "historical_series": [],
                "forecast": [],
            }

        current_average = current_average or (
            historical_series[-1]["average_price"] if historical_series else 0.0
        )

        regression = self._weighted_regression(historical_series)
        monthly_trend_value = regression["slope"]
        monthly_trend_pct = (
            (monthly_trend_value / current_average) * 100 if current_average else 0.0
        )

        volatility_pct = market_snapshot["volatility_pct"]
        momentum_pct = market_snapshot["momentum_pct"]
        seasonality_factors = market_snapshot["seasonality_factors"]
        anchor_date = market_snapshot["anchor_date"]

        net_external_pressure = event_impact["net_price_pressure_pct"]
        forecast_points = []

        horizon = max(1, min(int(forecast_months or 6), 60))
        base_confidence = self._calculate_confidence(
            sample_size=market_snapshot["matching_annonces"],
            series_points=len(historical_series),
            volatility_pct=volatility_pct,
            has_external_context=bool(event_impact["factors"]),
        )

        for step in range(1, horizon + 1):
            target_date = self._add_months(anchor_date, step)
            seasonal_pct = seasonality_factors.get(target_date.month, 0.0) * 100
            progressive_external_pct = (
                net_external_pressure * min(step / max(horizon, 1), 1.0) * 0.65
            )
            momentum_component = momentum_pct * min(step, 3) * 0.25
            projected_change_pct = (
                (monthly_trend_pct * step)
                + seasonal_pct
                + progressive_external_pct
                + momentum_component
            )

            predicted_price = current_average * (1 + (projected_change_pct / 100.0))
            predicted_price = max(round(predicted_price, 2), 1000.0)

            spread_pct = max(2.5, min(18.0, volatility_pct + (step * 0.6)))
            confidence = max(25, min(95, int(base_confidence - (step - 1) * 2)))

            forecast_points.append(
                {
                    "period": target_date.strftime("%Y-%m"),
                    "label": target_date.strftime("%b %Y"),
                    "predicted_price": round(predicted_price, 2),
                    "min_price": round(predicted_price * (1 - (spread_pct / 100.0)), 2),
                    "max_price": round(predicted_price * (1 + (spread_pct / 100.0)), 2),
                    "change_vs_current_pct": round(projected_change_pct, 2),
                    "seasonality_pct": round(seasonal_pct, 2),
                    "external_pressure_pct": round(progressive_external_pct, 2),
                    "confidence": confidence,
                }
            )

        forecast_prices = [point["predicted_price"] for point in forecast_points]
        average_forecast_price = round(mean(forecast_prices), 2) if forecast_prices else 0.0
        max_variation = max(abs(point["change_vs_current_pct"]) for point in forecast_points)
        trend_direction = self._resolve_trend_direction(monthly_trend_pct + net_external_pressure)

        summary = (
            f"Tendance {trend_direction} estimee sur {horizon} mois, "
            f"avec un prix moyen projete a {average_forecast_price:.0f} EUR."
        )

        return {
            "summary": summary,
            "current_average_price": round(current_average, 2),
            "forecast_horizon_months": horizon,
            "trend_direction": trend_direction,
            "trend_strength_pct": round(max_variation, 2),
            "monthly_trend_pct": round(monthly_trend_pct, 2),
            "volatility_pct": round(volatility_pct, 2),
            "confidence": base_confidence,
            "historical_series": historical_series,
            "forecast": forecast_points,
        }

    def identify_best_periods(
        self,
        market_snapshot: Dict[str, Any],
        price_forecast: Dict[str, Any],
    ) -> Dict[str, Any]:
        forecast_points = price_forecast.get("forecast", [])
        current_average = price_forecast.get("current_average_price", 0.0)

        if not forecast_points:
            return {
                "achat": [],
                "vente": [],
                "action_recommandee": {
                    "achat": "attendre_des_donnees",
                    "vente": "attendre_des_donnees",
                    "rationale": "Le systeme manque d'historique pour recommander une fenetre.",
                },
            }

        prices = [point["predicted_price"] for point in forecast_points]
        min_price = min(prices)
        max_price = max(prices)
        price_range = max(max_price - min_price, 1.0)
        good_deal_ratio = market_snapshot.get("good_deal_ratio", 0.0)

        scored_buy_windows = []
        scored_sell_windows = []

        for index, point in enumerate(forecast_points):
            future_prices = prices[index + 1 :] or [point["predicted_price"]]
            future_max = max(future_prices)
            future_min = min(future_prices)

            buy_score = (
                ((max_price - point["predicted_price"]) / price_range) * 65
                + (max(future_max - point["predicted_price"], 0) / price_range) * 25
                + (good_deal_ratio * 10)
            )

            sell_score = (
                ((point["predicted_price"] - min_price) / price_range) * 65
                + (max(point["predicted_price"] - future_min, 0) / price_range) * 25
                + ((100 - point["confidence"]) * 0.1)
            )

            scored_buy_windows.append((buy_score, point))
            scored_sell_windows.append((sell_score, point))

        achat = [
            self._build_period_payload(label="achat", point=point, score=score)
            for score, point in sorted(scored_buy_windows, key=lambda item: item[0], reverse=True)[:2]
        ]
        vente = [
            self._build_period_payload(label="vente", point=point, score=score)
            for score, point in sorted(scored_sell_windows, key=lambda item: item[0], reverse=True)[:2]
        ]

        best_buy = achat[0] if achat else None
        best_sell = vente[0] if vente else None
        trend_direction = price_forecast.get("trend_direction", "stable")

        if trend_direction == "hausse" and current_average and best_buy:
            achat_action = "acheter_maintenant"
            achat_reason = "Les prix devraient monter, acheter avant la hausse reduit le cout d'entree."
        elif trend_direction == "baisse":
            achat_action = "attendre"
            achat_reason = "La projection suggere un assouplissement des prix dans les prochains mois."
        else:
            achat_action = "surveiller"
            achat_reason = "Le marche reste equilibre, surveiller les prochaines publications est prudent."

        if trend_direction == "baisse" and current_average:
            vente_action = "vendre_maintenant"
            vente_reason = "La pression baissiere favorise une cession rapide avant une correction plus forte."
        elif trend_direction == "hausse":
            vente_action = "attendre_point_haut"
            vente_reason = "Le marche reste oriente a la hausse, une vente plus tardive peut mieux valoriser l'actif."
        else:
            vente_action = "surveiller"
            vente_reason = "La fenetre de vente dependra surtout des nouvelles annonces et evenements externes."

        return {
            "achat": achat,
            "vente": vente,
            "action_recommandee": {
                "achat": achat_action,
                "vente": vente_action,
                "rationale": f"{achat_reason} {vente_reason}",
                "meilleur_moment_achat": best_buy["label"] if best_buy else None,
                "meilleur_moment_vente": best_sell["label"] if best_sell else None,
            },
        }

    def evaluate_external_impacts(
        self,
        filters: Optional[Dict[str, Any]] = None,
        external_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        filters = self._clean_filters(filters)
        normalized = self._normalize_external_context(external_context)

        fuel_filter = filters.get("carburant")
        factors: List[Dict[str, Any]] = []

        economic = normalized.get("economic", {})
        weather = normalized.get("weather", {})
        events = normalized.get("events", [])

        inflation_rate = self._to_float(economic.get("inflation_rate"))
        if inflation_rate is not None and inflation_rate > 3:
            delta = min((inflation_rate - 3) * 0.45, 5.0)
            factors.append(
                self._factor_payload(
                    name="Inflation",
                    source="economic",
                    delta_pct=delta,
                    confidence=72,
                    explanation="Une inflation elevee augmente les couts de remplacement et soutient les prix affiches.",
                )
            )

        interest_rate = self._to_float(economic.get("interest_rate"))
        if interest_rate is not None:
            delta = 0.0
            if interest_rate > 4:
                delta = -min((interest_rate - 4) * 0.55, 4.5)
            elif interest_rate < 2:
                delta = min((2 - interest_rate) * 0.35, 2.0)
            if delta:
                factors.append(
                    self._factor_payload(
                        name="Taux de financement",
                        source="economic",
                        delta_pct=delta,
                        confidence=68,
                        explanation="Le cout du credit agit directement sur la demande solvable.",
                    )
                )

        exchange_pressure = self._to_float(
            economic.get("exchange_rate_pressure")
            or economic.get("fx_pressure")
            or economic.get("currency_pressure")
        )
        if exchange_pressure:
            delta = min(max(exchange_pressure, -5.0), 5.0) * 0.6
            factors.append(
                self._factor_payload(
                    name="Pression de change",
                    source="economic",
                    delta_pct=delta,
                    confidence=65,
                    explanation="Les variations de devise influencent le cout des vehicules importes.",
                )
            )

        consumer_confidence_delta = self._extract_confidence_delta(economic)
        if consumer_confidence_delta:
            delta = max(min(consumer_confidence_delta * 0.12, 3.0), -3.0)
            factors.append(
                self._factor_payload(
                    name="Confiance des consommateurs",
                    source="economic",
                    delta_pct=delta,
                    confidence=62,
                    explanation="Une confiance plus forte stimule la demande de vehicules, surtout sur l'occasion recente.",
                )
            )

        fuel_price_change = self._to_float(economic.get("fuel_price_change_pct"))
        if fuel_price_change:
            if fuel_filter in {"essence", "diesel"}:
                delta = -min(fuel_price_change * 0.12, 4.0)
            elif fuel_filter in {"hybride", "electrique"}:
                delta = min(fuel_price_change * 0.09, 3.0)
            else:
                delta = -min(fuel_price_change * 0.04, 1.5)
            factors.append(
                self._factor_payload(
                    name="Variation du prix du carburant",
                    source="economic",
                    delta_pct=delta,
                    confidence=66,
                    explanation="Le cout d'usage modifie l'attractivite relative des motorisations.",
                )
            )

        weather_severity = self._to_float(
            weather.get("severity_index") or weather.get("weather_severity")
        )
        if weather_severity:
            delta = min(weather_severity / 35.0, 3.0)
            factors.append(
                self._factor_payload(
                    name="Perturbation meteo",
                    source="weather",
                    delta_pct=delta,
                    confidence=55,
                    explanation="Les perturbations logistiques peuvent reduire l'offre disponible a court terme.",
                )
            )

        rainfall_anomaly = self._to_float(weather.get("rainfall_anomaly_pct"))
        if rainfall_anomaly:
            delta = min(max(rainfall_anomaly, 0.0) * 0.03, 1.8)
            if delta:
                factors.append(
                    self._factor_payload(
                        name="Anomalie de precipitations",
                        source="weather",
                        delta_pct=delta,
                        confidence=48,
                        explanation="Des conditions plus difficiles freinent les transactions et la logistique locale.",
                    )
                )

        for event in events:
            factor = self._event_to_factor(event=event, fuel_filter=fuel_filter)
            if factor:
                factors.append(factor)

        factors.sort(key=lambda item: abs(item["delta_pct"]), reverse=True)
        net_pressure = round(sum(item["delta_pct"] for item in factors), 2)

        return {
            "market_bias": self._resolve_trend_direction(net_pressure),
            "net_price_pressure_pct": net_pressure,
            "factors": factors,
            "top_drivers": [item["name"] for item in factors[:3]],
            "normalized_context": normalized,
        }

    def generate_market_insights(
        self,
        filters: Optional[Dict[str, Any]] = None,
        market_snapshot: Optional[Dict[str, Any]] = None,
        price_forecast: Optional[Dict[str, Any]] = None,
        event_impact: Optional[Dict[str, Any]] = None,
        best_periods: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        filters = self._clean_filters(filters)
        queryset = self._build_queryset(filters)
        market_snapshot = market_snapshot or self._build_market_snapshot(queryset, 12)
        event_impact = event_impact or self.evaluate_external_impacts(filters=filters)
        price_forecast = price_forecast or self.predict_market_prices(
            filters=filters,
            queryset=queryset,
            market_snapshot=market_snapshot,
            event_impact=event_impact,
        )
        best_periods = best_periods or self.identify_best_periods(
            market_snapshot=market_snapshot,
            price_forecast=price_forecast,
        )

        insights = []

        direction = price_forecast["trend_direction"]
        projected_change = (
            price_forecast["forecast"][0]["change_vs_current_pct"]
            if price_forecast.get("forecast")
            else 0.0
        )
        insights.append(
            {
                "titre": f"Tendance du marche: {direction}",
                "description": (
                    f"Projection a court terme de {projected_change:+.1f}% "
                    f"avec une confiance de {price_forecast['confidence']}%."
                ),
                "type": "tendance_prix",
                "niveau_impact": min(90, max(35, int(abs(projected_change) * 8) or 40)),
                "confiance": price_forecast["confidence"],
                "marques_concernees": [item["marque"] for item in market_snapshot["top_brands"][:3]],
                "categories_vehicules": self._extract_categories(filters),
                "fourchettes_prix": market_snapshot["price_range"],
            }
        )

        if best_periods.get("achat"):
            best_buy = best_periods["achat"][0]
            insights.append(
                {
                    "titre": f"Fenetre achat: {best_buy['label']}",
                    "description": (
                        f"Prix cible projete a {best_buy['predicted_price']:.0f} EUR "
                        f"avec un score d'opportunite de {best_buy['score']}."
                    ),
                    "type": "conseil_achat",
                    "niveau_impact": min(90, max(40, int(best_buy["score"]))),
                    "confiance": best_buy["confidence"],
                    "marques_concernees": [item["marque"] for item in market_snapshot["top_brands"][:2]],
                    "categories_vehicules": self._extract_categories(filters),
                    "fourchettes_prix": market_snapshot["price_range"],
                }
            )

        if best_periods.get("vente"):
            best_sell = best_periods["vente"][0]
            insights.append(
                {
                    "titre": f"Fenetre vente: {best_sell['label']}",
                    "description": (
                        f"Niveau cible a {best_sell['predicted_price']:.0f} EUR, "
                        f"interessant pour maximiser la valorisation."
                    ),
                    "type": "conseil_vente",
                    "niveau_impact": min(90, max(40, int(best_sell["score"]))),
                    "confiance": best_sell["confidence"],
                    "marques_concernees": [item["marque"] for item in market_snapshot["top_brands"][:2]],
                    "categories_vehicules": self._extract_categories(filters),
                    "fourchettes_prix": market_snapshot["price_range"],
                }
            )

        if event_impact.get("factors"):
            main_driver = event_impact["factors"][0]
            insights.append(
                {
                    "titre": f"Impact externe: {main_driver['name']}",
                    "description": (
                        f"Effet estime de {main_driver['delta_pct']:+.1f}% sur les prix. "
                        f"{main_driver['explanation']}"
                    ),
                    "type": "prediction",
                    "niveau_impact": min(95, max(35, int(abs(main_driver["delta_pct"]) * 20))),
                    "confiance": main_driver["confidence"],
                    "marques_concernees": [item["marque"] for item in market_snapshot["top_brands"][:2]],
                    "categories_vehicules": self._extract_categories(filters),
                    "fourchettes_prix": market_snapshot["price_range"],
                }
            )

        return insights[:4]

    def _build_queryset(self, filters: Optional[Dict[str, Any]] = None):
        filters = self._clean_filters(filters)
        base_queryset = Annonce.objects.select_related("vehicule")

        active_queryset = base_queryset.filter(est_active=True)
        queryset = active_queryset if active_queryset.exists() else base_queryset

        marque = filters.get("marque")
        if marque:
            queryset = queryset.filter(vehicule__marque__iexact=marque)

        marques = filters.get("marques")
        if marques:
            queryset = queryset.filter(vehicule__marque__in=marques)

        modele = filters.get("modele")
        if modele:
            queryset = queryset.filter(vehicule__modele__iexact=modele)

        category = filters.get("categorie")
        if category:
            queryset = queryset.filter(vehicule__categorie__iexact=category)

        carburant = filters.get("carburant")
        if carburant:
            queryset = queryset.filter(carburant__iexact=carburant)

        pays = filters.get("pays")
        if pays:
            queryset = queryset.filter(pays__iexact=pays)

        vehicule_id = filters.get("vehicule_id")
        if vehicule_id:
            queryset = queryset.filter(vehicule_id=vehicule_id)

        annee_min = self._to_int(filters.get("annee_min"))
        if annee_min:
            queryset = queryset.filter(annee__gte=annee_min)

        annee_max = self._to_int(filters.get("annee_max"))
        if annee_max:
            queryset = queryset.filter(annee__lte=annee_max)

        prix_min = self._to_float(filters.get("prix_min"))
        if prix_min is not None:
            queryset = queryset.filter(prix__gte=prix_min)

        prix_max = self._to_float(filters.get("prix_max"))
        if prix_max is not None:
            queryset = queryset.filter(prix__lte=prix_max)

        return queryset

    def _build_market_snapshot(
        self,
        queryset,
        lookback_months: int,
    ) -> Dict[str, Any]:
        lookback_months = max(3, min(int(lookback_months or 12), 36))
        anchor_date = self._month_start(timezone.now())
        start_date = self._add_months(anchor_date, -lookback_months)

        recent_queryset = queryset.filter(date_publication__gte=start_date)
        if recent_queryset.count() < 3:
            recent_queryset = queryset

        aggregates = recent_queryset.aggregate(
            average_price=Avg("prix"),
            min_price=Min("prix"),
            max_price=Max("prix"),
            listing_count=Count("id"),
            good_deals=Count("id", filter=Q(est_bonne_affaire=True)),
        )

        average_price = float(aggregates["average_price"] or 0.0)
        min_price = float(aggregates["min_price"] or 0.0)
        max_price = float(aggregates["max_price"] or 0.0)
        listing_count = int(aggregates["listing_count"] or 0)
        good_deals = int(aggregates["good_deals"] or 0)
        good_deal_ratio = round((good_deals / listing_count) * 100, 2) if listing_count else 0.0

        monthly_series_queryset = (
            recent_queryset.annotate(period=TruncMonth("date_publication"))
            .values("period")
            .annotate(
                average_price=Avg("prix"),
                min_price=Min("prix"),
                max_price=Max("prix"),
                listing_count=Count("id"),
                good_deals=Count("id", filter=Q(est_bonne_affaire=True)),
            )
            .order_by("period")
        )

        historical_series = []
        seasonal_buckets: Dict[int, List[float]] = {}
        historical_prices = []

        for item in monthly_series_queryset:
            period = item["period"]
            average = float(item["average_price"] or 0.0)
            count = int(item["listing_count"] or 0)
            deals = int(item["good_deals"] or 0)
            deal_ratio = round((deals / count) * 100, 2) if count else 0.0
            historical_prices.append(average)
            seasonal_buckets.setdefault(period.month, []).append(average)

            historical_series.append(
                {
                    "period": period.strftime("%Y-%m"),
                    "label": period.strftime("%b %Y"),
                    "average_price": round(average, 2),
                    "min_price": round(float(item["min_price"] or average), 2),
                    "max_price": round(float(item["max_price"] or average), 2),
                    "listing_count": count,
                    "good_deal_ratio": deal_ratio,
                }
            )

        momentum_pct = 0.0
        pct_changes = []
        for index in range(1, len(historical_prices)):
            previous = historical_prices[index - 1]
            current = historical_prices[index]
            if previous:
                pct_changes.append(((current - previous) / previous) * 100)

        if pct_changes:
            momentum_pct = mean(pct_changes[-2:])

        volatility_pct = round(pstdev(pct_changes), 2) if len(pct_changes) > 1 else 0.0
        overall_average = average_price or (mean(historical_prices) if historical_prices else 0.0)

        seasonality_factors = {}
        if overall_average:
            for month, values in seasonal_buckets.items():
                seasonality_factors[month] = (mean(values) / overall_average) - 1

        top_brands = list(
            recent_queryset.values("vehicule__marque")
            .annotate(
                marque=Max("vehicule__marque"),
                listing_count=Count("id"),
                average_price=Avg("prix"),
            )
            .order_by("-listing_count")[:5]
        )
        top_brands_payload = [
            {
                "marque": item["marque"] or item["vehicule__marque"] or "Inconnu",
                "listing_count": int(item["listing_count"] or 0),
                "average_price": round(float(item["average_price"] or 0.0), 2),
            }
            for item in top_brands
        ]

        fuel_mix_queryset = list(
            recent_queryset.values("carburant")
            .annotate(listing_count=Count("id"), average_price=Avg("prix"))
            .order_by("-listing_count")[:5]
        )
        fuel_mix = [
            {
                "carburant": item["carburant"] or "inconnu",
                "listing_count": int(item["listing_count"] or 0),
                "average_price": round(float(item["average_price"] or 0.0), 2),
            }
            for item in fuel_mix_queryset
        ]

        sorted_prices = sorted(historical_prices)
        median_proxy_price = 0.0
        if sorted_prices:
            median_proxy_price = sorted_prices[len(sorted_prices) // 2]

        return {
            "matching_annonces": listing_count,
            "current_average_price": round(average_price, 2),
            "median_proxy_price": round(float(median_proxy_price or average_price), 2),
            "price_range": {
                "min": round(min_price, 2),
                "max": round(max_price, 2),
            },
            "good_deal_ratio": good_deal_ratio,
            "historical_series": historical_series,
            "top_brands": top_brands_payload,
            "fuel_mix": fuel_mix,
            "volatility_pct": volatility_pct,
            "momentum_pct": round(momentum_pct, 2),
            "seasonality_factors": seasonality_factors,
            "anchor_date": anchor_date,
        }

    def _build_custom_trends(
        self,
        filters: Dict[str, Any],
        market_snapshot: Dict[str, Any],
        price_forecast: Dict[str, Any],
        best_periods: Dict[str, Any],
        personalization_notes: List[str],
    ) -> Dict[str, Any]:
        top_brands = market_snapshot.get("top_brands", [])
        buy_window = best_periods.get("achat", [])
        sell_window = best_periods.get("vente", [])

        watchlist = []
        for brand in top_brands[:3]:
            watchlist.append(
                {
                    "segment": brand["marque"],
                    "listing_count": brand["listing_count"],
                    "average_price": brand["average_price"],
                    "signal": "surveiller_hausse"
                    if price_forecast["trend_direction"] == "hausse"
                    else "surveiller_repli",
                }
            )

        recommendations = []
        if buy_window:
            recommendations.append(
                f"Prioriser les achats autour de {buy_window[0]['label']} pour capter le meilleur point d'entree."
            )
        if sell_window:
            recommendations.append(
                f"Planifier une vente vers {sell_window[0]['label']} pour profiter du niveau de prix projete."
            )
        if market_snapshot["good_deal_ratio"] >= 20:
            recommendations.append(
                "Le taux de bonnes affaires est eleve; augmenter la frequence de veille peut accelerer une bonne acquisition."
            )
        if not recommendations:
            recommendations.append(
                "Le marche reste stable; definir des alertes sur les segments favoris reste la meilleure approche."
            )

        return {
            "personalization_used": bool(personalization_notes),
            "personalization_notes": personalization_notes,
            "watchlist": watchlist,
            "recommendations": recommendations[:3],
        }

    def _apply_profile_defaults(self, filters: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        if not self.user:
            return filters, []

        notes = []

        try:
            profile = UserProfileAnalysis.objects.filter(user=self.user).first()
        except Exception:
            profile = None

        if not profile:
            return filters, notes

        if not filters.get("prix_max") and profile.budget_max:
            filters["prix_max"] = float(profile.budget_max)
            notes.append("Budget max du profil applique.")

        if not filters.get("prix_min") and profile.budget_min:
            filters["prix_min"] = float(profile.budget_min)
            notes.append("Budget min du profil applique.")

        if not filters.get("carburant") and profile.preferences_carburant:
            filters["carburant"] = profile.preferences_carburant[0]
            notes.append("Preference carburant du profil appliquee.")

        if not filters.get("categorie") and profile.types_vehicule:
            filters["categorie"] = profile.types_vehicule[0]
            notes.append("Type de vehicule prefere applique.")

        if not filters.get("marque"):
            try:
                marque_names = list(
                    profile.marques_preferrees.values_list("nom", flat=True)[:1]
                )
            except Exception:
                marque_names = []
            if marque_names:
                filters["marque"] = marque_names[0]
                notes.append("Marque preferee du profil appliquee.")

        return filters, notes

    def _normalize_external_context(
        self, external_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if not external_context:
            return {"economic": {}, "weather": {}, "events": []}

        return {
            "economic": external_context.get("economic")
            or external_context.get("economy")
            or external_context.get("economic_indicators")
            or {},
            "weather": external_context.get("weather")
            or external_context.get("weather_data")
            or external_context.get("weather_indicators")
            or {},
            "events": external_context.get("events")
            or external_context.get("economic_events")
            or [],
        }

    def _event_to_factor(self, event: Dict[str, Any], fuel_filter: Optional[str]):
        if not isinstance(event, dict):
            return None

        magnitude = self._to_float(event.get("magnitude"))
        sensitivity = self._to_float(event.get("price_sensitivity"))
        confidence = self._to_int(event.get("confidence")) or 58
        name = event.get("label") or event.get("name") or "Evenement externe"
        direction = str(
            event.get("direction") or event.get("impact_direction") or "increase"
        ).lower()
        target = str(event.get("target") or event.get("scope") or "all").lower()

        if magnitude is None:
            magnitude = 1.0
        if sensitivity is None:
            sensitivity = 1.8

        sign = 1.0
        if direction in {"decrease", "down", "baisse", "negative"}:
            sign = -1.0

        delta = sign * magnitude * sensitivity
        if target not in {"all", "", "marche"} and fuel_filter and target != fuel_filter:
            delta *= 0.35

        return self._factor_payload(
            name=name,
            source="event",
            delta_pct=round(delta, 2),
            confidence=max(35, min(90, confidence)),
            explanation=event.get("description")
            or "Effet manuel applique a partir du contexte externe fourni.",
        )

    def _weighted_regression(self, historical_series: List[Dict[str, Any]]) -> Dict[str, float]:
        if len(historical_series) < 2:
            return {"slope": 0.0, "intercept": 0.0}

        x_values = list(range(len(historical_series)))
        y_values = [item["average_price"] for item in historical_series]
        weights = [index + 1 for index in x_values]

        weight_sum = sum(weights)
        mean_x = sum(weight * value for weight, value in zip(weights, x_values)) / weight_sum
        mean_y = sum(weight * value for weight, value in zip(weights, y_values)) / weight_sum

        numerator = sum(
            weight * (x_value - mean_x) * (y_value - mean_y)
            for weight, x_value, y_value in zip(weights, x_values, y_values)
        )
        denominator = sum(
            weight * ((x_value - mean_x) ** 2)
            for weight, x_value in zip(weights, x_values)
        )

        slope = numerator / denominator if denominator else 0.0
        intercept = mean_y - (slope * mean_x)
        return {"slope": slope, "intercept": intercept}

    def _calculate_confidence(
        self,
        sample_size: int,
        series_points: int,
        volatility_pct: float,
        has_external_context: bool,
    ) -> int:
        confidence = 35
        confidence += min(sample_size, 80) * 0.35
        confidence += min(series_points, 12) * 2
        confidence -= min(volatility_pct, 20) * 1.4
        if has_external_context:
            confidence += 4
        return max(25, min(92, int(confidence)))

    def _resolve_trend_direction(self, value: float) -> str:
        if value > 1:
            return "hausse"
        if value < -1:
            return "baisse"
        return "stable"

    def _extract_categories(self, filters: Dict[str, Any]) -> List[str]:
        categories = []
        if filters.get("categorie"):
            categories.append(filters["categorie"])
        if filters.get("carburant"):
            categories.append(filters["carburant"])
        return categories[:3]

    def _build_period_payload(self, label: str, point: Dict[str, Any], score: float) -> Dict[str, Any]:
        return {
            "type": label,
            "label": point["label"],
            "period": point["period"],
            "predicted_price": point["predicted_price"],
            "change_vs_current_pct": point["change_vs_current_pct"],
            "confidence": point["confidence"],
            "score": round(score, 1),
        }

    def _factor_payload(
        self,
        name: str,
        source: str,
        delta_pct: float,
        confidence: int,
        explanation: str,
    ) -> Dict[str, Any]:
        return {
            "name": name,
            "source": source,
            "delta_pct": round(delta_pct, 2),
            "confidence": confidence,
            "explanation": explanation,
        }

    def _extract_confidence_delta(self, economic: Dict[str, Any]) -> float:
        delta = self._to_float(economic.get("consumer_confidence_delta"))
        if delta is not None:
            return delta

        absolute_value = self._to_float(economic.get("consumer_confidence"))
        if absolute_value is None:
            return 0.0

        if abs(absolute_value) <= 10:
            return absolute_value
        return absolute_value - 100

    def _clean_filters(self, filters: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        cleaned = {}
        for key, value in (filters or {}).items():
            if value in (None, "", [], {}):
                continue
            cleaned[key] = value
        return cleaned

    def _month_start(self, value: datetime) -> datetime:
        return value.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def _add_months(self, value: datetime, months: int) -> datetime:
        total_months = (value.year * 12) + (value.month - 1) + months
        target_year = total_months // 12
        target_month = (total_months % 12) + 1
        target_day = min(value.day, calendar.monthrange(target_year, target_month)[1])
        return value.replace(year=target_year, month=target_month, day=target_day)

    def _to_float(self, value: Any) -> Optional[float]:
        if value in (None, ""):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _to_int(self, value: Any) -> Optional[int]:
        if value in (None, ""):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
