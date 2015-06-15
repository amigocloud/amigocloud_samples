package com.amigocloud;

public class Main {

    // The API_TOKEN should be generated here: https://www.amigocloud.com/accounts/tokens
    private static final String API_TOKEN = "";

    // User ID can be found here: https://www.amigocloud.com/api/v1/me
    private static long userID = 0;

    private static class MyAmigoWebsocketListener implements AmigoWebsocketListener {
        @Override
        public void onMessage(String message) {
            System.out.println("onMessage(): " + message);
        }
    }

    public static void testWebsockets() {
        AmigoWebsockets socket = new AmigoWebsockets(userID, API_TOKEN, new MyAmigoWebsocketListener());
        socket.connect();
    }

    public static void testRealitimeWebsockets() {
        long projectID = 0;
        long datasetID = 0;
        AmigoWebsockets socket = new AmigoWebsockets(userID, projectID, datasetID, API_TOKEN, new MyAmigoWebsocketListener());
        socket.connect();
    }

    public static void main(String[] args) {
        System.out.println("AmigoCloud Websockets sample");

        testWebsockets();

//        testRealitimeWebsockets();
    }
}
