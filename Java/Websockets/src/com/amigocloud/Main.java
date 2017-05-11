package com.amigocloud;

import java.sql.Time;
import java.util.Timer;

public class Main {

    // The API_TOKEN should be generated here: https://www.amigocloud.com/accounts/tokens
    private static final String API_TOKEN = "<token>";

    // User ID can be found here: https://www.amigocloud.com/api/v1/me
    private static long userID = 0;
    private static long projectID = 0;
    private static long datasetID = 0;

    // Can be found here: https://www.amigocloud.com/api/v1/settings
    private static String url = "https://www.amigocloud.com";
    private static String path = "/v2_socket.io";

    private static AmigoWebsocketListener listener = new AmigoWebsocketListener() {

        @Override
        public void onMessage(String message) {
            System.out.println("onMessage(): " + message);
        }

        @Override
        public void onClose(int code, String reason) {
            System.out.println("onClose(): " + code + ", " + reason);
        }
    };

    public static void testWebsockets() {
        SocketIOClient socket = new SocketIOClient(url, userID, -1, -1, API_TOKEN, listener);
        socket.connect(path);
    }

    public static void testRealitimeWebsockets() {

        SocketIOClient socket = new SocketIOClient(url, userID, projectID, datasetID, API_TOKEN, listener);
        socket.connect(path);
    }

    public static void main(String[] args) {
        System.out.println("AmigoCloud Websockets sample");

//        testWebsockets();
        testRealitimeWebsockets();
    }
}
