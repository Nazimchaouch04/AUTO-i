import stripe
from django.conf import settings
from decouple import config

stripe.api_key = config('STRIPE_SECRET_KEY', default='sk_test_...')

STRIPE_PRICES = {
    'pro': config('STRIPE_PRICE_PRO', default='price_pro_id'),
    'business': config('STRIPE_PRICE_BUSINESS', default='price_business_id'),
}

def create_checkout_session(user, plan_nom, success_url, cancel_url):
    try:
        abonnement = user.subscription
        customer_id = getattr(abonnement, 'stripe_customer_id', None)

        if not customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.username,
                metadata={'user_id': user.id}
            )
            customer_id = customer.id
            abonnement.stripe_customer_id = customer_id
            abonnement.save()

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{'price': STRIPE_PRICES[plan_nom], 'quantity': 1}],
            mode='subscription',
            success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url,
            metadata={'user_id': user.id, 'plan_nom': plan_nom}
        )
        return {'url': session.url, 'session_id': session.id}

    except stripe.error.StripeError as e:
        raise Exception(f"Erreur Stripe: {e.user_message}")


def handle_webhook(payload, sig_header):
    webhook_secret = config('STRIPE_WEBHOOK_SECRET', default='')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        return None

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        plan_nom = session['metadata']['plan_nom']

        from django.contrib.auth.models import User
        from apps.subscriptions.models import Plan, Abonnement

        user = User.objects.get(id=user_id)
        plan = Plan.objects.get(nom=plan_nom)
        abonnement = user.subscription
        abonnement.plan = plan
        abonnement.actif = True
        abonnement.stripe_subscription_id = session.get('subscription', '')
        abonnement.save()

        if hasattr(user, 'profil'):
            bonus = {'pro': 200, 'business': 500}.get(plan_nom, 0)
            if bonus:
                user.profil.add_coins(bonus)

    elif event['type'] == 'customer.subscription.deleted':
        sub_id = event['data']['object']['id']
        from apps.subscriptions.models import Abonnement, Plan
        try:
            abonnement = Abonnement.objects.get(stripe_subscription_id=sub_id)
            abonnement.plan = Plan.objects.get(nom='free')
            abonnement.actif = False
            abonnement.save()
        except Abonnement.DoesNotExist:
            pass

    return event['type']
