@isTest
private class OrderHandler_Test {
    @isTest
    static void testCreateOrder() {
        String result = OrderHandler.createOrder('PROD-001', 5);
        Assert.areEqual('Order Confirmed', result, 'The message should be Order Confirmed');
    }
}
