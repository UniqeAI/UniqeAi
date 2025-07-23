from fastapi import APIRouter, HTTPException
from backend.app.services import mock_tools

router = APIRouter(prefix="/mock-test", tags=["MockTest"])

@router.get("/user/{user_id}")
def test_get_user_info(user_id: int):
    return mock_tools.getUserInfo(user_id)

@router.get("/packages")
def test_get_available_packages():
    return mock_tools.getAvailablePackages()

@router.get("/invoice/{user_id}")
def test_get_invoice(user_id: int):
    return mock_tools.getInvoice(user_id)

@router.get("/customer/{user_id}")
def test_get_customer_info(user_id: int):
    return mock_tools.getCustomerInfo(user_id)

@router.get("/payments/{user_id}")
def test_get_payment_history(user_id: int):
    return mock_tools.getPaymentHistory(user_id)

@router.get("/subscription/{user_id}")
def test_get_subscription_status(user_id: int):
    return mock_tools.getSubscriptionStatus(user_id)

@router.get("/support/{user_id}")
def test_get_support_tickets(user_id: int):
    return mock_tools.getSupportTickets(user_id)

@router.get("/address/{user_id}")
def test_get_address(user_id: int):
    return mock_tools.getAddress(user_id)

@router.get("/campaigns")
def test_get_campaigns():
    return mock_tools.getCampaigns() 