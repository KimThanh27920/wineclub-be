
import stripe
from django.conf import settings
from dotenv import load_dotenv
from rest_framework.response import Response
from bases.exception.exceptions import response_exception
from datetime import datetime

from operator import itemgetter
load_dotenv()

stripe.api_key = settings.STRIPE_SECRET_KEY



class StripeAPI:

    # create price subscription package 
    def create_price(name, price, currency, interval,interval_count,subpk):
        product_id = stripe.Product.create(name=name,metadata={"subscription_package": subpk})
        price_id = stripe.Price.create(
            unit_amount= price, 
            currency=currency,
            recurring={
                "interval": interval,
                "interval_count": interval_count
                },
            product=product_id,
            metadata={"subscription_package": subpk},
            )
        return price_id.id

    # Update price subcription package
    def delete_price(sub_id):
        query = "metadata['subscription_package']:'"+ str(sub_id)+"'"
       
        search =  stripe.Product.search(query=query )
        for item in search["data"]:
            stripe.Product.modify(str(item["id"]),active=False)
        
        search_price = stripe.Price.search( query = query)
        for item in search_price["data"]:
            stripe.Price.modify(str(item["id"]), active=False)
 

    # checkout subscription
    def subscription_checkout(stripe_account, price_id, user_id):
        try:
            subscription = stripe.Subscription.create(
                customer = stripe_account,
                items=[
                    {"price": price_id },
                ],
                metadata={
                    "account": user_id
                    }
            )
            data = {
                "id": subscription["id"],
                "created": datetime.fromtimestamp(subscription["created"]),
                "unit_amount": float(subscription["items"]["data"][0]["price"]["unit_amount"])/100,
                "currency":subscription["currency"],
                "interval": subscription["items"]["data"][0]["price"]["recurring"]["interval"],
                "interval_amount": subscription["items"]["data"][0]["price"]["recurring"]["interval_count"],
                "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
                "status": subscription["status"],
                "metadata": subscription["metadata"]
            }
        except stripe.error.InvalidRequestError:
            data = {"status": "Failed"}
            return data
        return data

    def subscription_search(user_id):
        query = "status:'active' AND metadata['account']:'"+ str(user_id)+"'"
        search = stripe.Subscription.search(query=query)
        data = search["data"]
        return data
    
    def cancel(user_id):
        try :
            query = "status:'active' AND metadata['account']:'"+ str(user_id)+"'"
            search = stripe.Subscription.search(query=query)
            data = search["data"]
            sorts = sorted(data,key=itemgetter('created'), reverse=True)
            canceled = stripe.Subscription.delete(
                    sorts[0]["items"]["data"][0]["subscription"],
            )
            data = {
                    "id": canceled["id"],
                    "created": datetime.fromtimestamp(canceled["created"]),
                    "unit_amount": float(canceled["items"]["data"][0]["price"]["unit_amount"])/100,
                    "currency":canceled["currency"],
                    "interval": canceled["items"]["data"][0]["price"]["recurring"]["interval"],
                    "interval_amount": canceled["items"]["data"][0]["price"]["recurring"]["interval_count"],
                    "next_payment_date": datetime.fromtimestamp(canceled["current_period_end"]),
                    "status": canceled["status"],
                    "metadata": canceled["metadata"]
                }

        except stripe.error.InvalidRequestError:
            data = {"status": "Failed"}
            return data
        return data


def stripe_customer_create(user):  # function created stripe customer
    try:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name
        )
    except Exception as e:
        return None
    return customer.id


def stripe_customer_search(user):  # function search stripe customer
    customer = stripe.Customer.search(
        query="email:'%s'" % (user.email),
    )
    if(len(customer.data) == 0):
        customer_id = stripe_customer_create(user)
    else:
        customer_id = customer.data[0].id
    return customer_id


# create PaymentIntent
def stripe_payment_intent_create(order, amount, user, customer, payment_method):
    try:
        payment = stripe.PaymentIntent.create(
            amount=amount*100,  # unit is cent
            currency="usd",
            payment_method=payment_method,
            payment_method_types=['card'],
            description="Payment",
            metadata={
                "order_id": order,
                "account_id": user
            },
            customer=customer
        )
    except stripe.error.CardError as e:
        return response_exception("card invalid, please choose another card")
    except stripe.error.InvalidRequestError as e:
        return response_exception("no such payment_method")
    except Exception as e:
        return response_exception("some error occurred try again later or choose another payment method")
    return Response(data=payment)


# confirm PaymentIntent
def stripe_payment_intent_confirm(payment_intent, payment_method):
    try:
        confirm = stripe.PaymentIntent.confirm(
            payment_intent,
            payment_method=payment_method,
        )
    except stripe.error.CardError as e:
        return response_exception("card invalid, please choose another card")
    except stripe.error.InvalidRequestError as e:
        return response_exception("no such payment_method")
    except Exception as e:
        # message = str(e)[(str(e).find(":", 0, len(str(e))))+2: len(str(e))]
        return response_exception("some error occurred try again later or choose another payment method")
    return Response(data=confirm)


# Function listen event from Stripe
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # Check valid payload with signature
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return e
    return event


def stripe_setup_intent(request):
    try:
        setup = stripe.SetupIntent.create(
            payment_method_types=["card"],
            customer=stripe_customer_search(request.user)
        )
    except Exception as e:
        return response_exception(e)
    return Response(data=setup)


def stripe_list_payment_method(request):
    try:
        payment_methods = stripe.Customer.list_payment_methods(
            stripe_customer_search(request.user),
            type="card",
        )
    except Exception as e:
        return response_exception(e)
    return Response(data=payment_methods)


def stripe_payment_intent_search(order_id):
    try:
        payment_intent = stripe.PaymentIntent.search(
            query="metadata['order_id']:'%s'" % (order_id),
        )
    except Exception as e:
        print(e)
        return response_exception(e)
    if(len(payment_intent.data) == 0):
        payment_intent = None
    else:
        payment_intent = payment_intent.data[0]
    return payment_intent


def stripe_refund(payment_intent):
    try:
        refund = stripe.Refund.create(
            payment_intent=payment_intent,
        )
    except Exception as e:
        return e
    return refund


def stripe_transaction(txn):  # call Transaction Stripe
    try:
        transaction = stripe.BalanceTransaction.retrieve(
            txn,
        )
    except Exception as e:
        return e
    return transaction


def stripe_created_connect(business_email, address_business, identity_verify, business_profile, bank_account):
    try:
        connect_account = stripe.Account.create(
            type="custom",
            country="US",
            email=business_email,
            business_type="individual",
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
            external_account={
                "object": "bank_account",
                "account_holder_name": bank_account["account_holder_name"],
                "account_holder_type": "individual",
                "country": "US",
                "currency": "usd",
                "routing_number": "110000000",
                "account_number": "000123456789",
            },
            individual={
                "address": {
                    "city": address_business["city"],
                    "country": address_business["country"],
                    "line1": address_business["line1"],
                    "line2": address_business["line2"],
                    "postal_code": address_business["postal_code"],
                    "state": address_business["state"]
                },
                "dob": {
                    "day": 1,
                    "month": 1,
                    "year": 1980
                },
                "email": business_email,
                "first_name": identity_verify["first_name"],
                "last_name": identity_verify["last_name"],
                "phone": "8888675309",
                "ssn_last_4": identity_verify["ssn_last_4"]
            },
            business_profile={
                "url": business_profile["url"],
                "mcc": business_profile["mcc"],
            },
            tos_acceptance={
                # "service_agreement": "recipient",
                "date": int(datetime.timestamp(datetime.now())),
                "ip": "127.0.0.1", #ip get to business
            },

        )
    except Exception as e:
        print(e)

    return connect_account


def stripe_retrieve_account(acct_id):
    try:
        account = stripe.Account.retrieve(acct_id)
    except Exception as e:
        pass
    return account


def stripe_created_account_link(account_connect):
    YOUR_DOMAIN = 'http://127.0.0.1:8000/'
    try:
        link = stripe.AccountLink.create(
            account=account_connect,
            refresh_url=YOUR_DOMAIN + 'success/',
            return_url=YOUR_DOMAIN + 'cancel/',
            type="account_onboarding",
        )
    except Exception as e:
        print(e)
    return link
