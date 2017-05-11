package com.amigocloud;


import io.socket.client.IO;
import io.socket.client.Socket;
import org.json.JSONObject;

class SocketIOClient {
    private Socket socket;
    private long userId;
    private long projectId = -1;
    private String websocket_token;
    private String apiToken;
    private String baseURL;
    private long datasetId = -1;
    private AmigoWebsocketListener listener = null;

    public SocketIOClient(String baseUrl, long userId, long projectID, long datasetID, String apiToken, AmigoWebsocketListener listener) {
        this.baseURL = baseUrl;
        this.userId = userId;
        this.projectId = projectID;
        this.datasetId = datasetID;
        this.apiToken = apiToken;
        this.listener = listener;
    }

    public void connect(String path) {
        if(datasetId < 0)
            fetchWebsocketsSession();
        else
            fetchWebsocketsSessionRealTime();

        IO.Options opts = new IO.Options();
        opts.path = path;
        try {
            socket = IO.socket(this.baseURL + "/amigosocket", opts);
        } catch (Exception e) {
            e.printStackTrace();
        }

        socket.on(Socket.EVENT_CONNECT, args -> {
            try {
                System.out.println("EVENT_CONNECT");
                JSONObject json = new JSONObject();
                json.put("userid", userId);
                json.put("websocket_session", websocket_token);
                if(datasetId > 0) json.put("datasetid", datasetId);
                socket.emit("authenticate", json);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).on(Socket.EVENT_CONNECT_ERROR, args -> {
            Exception err = (Exception)args[0];
            System.out.println("EVENT_CONNECT_ERROR " + err.getMessage());
            socket.disconnect();
        }).on(Socket.EVENT_CONNECTING, args -> {
            System.out.println("EVENT_CONNECTING ");
        }).on(Socket.EVENT_DISCONNECT, args -> System.out.println("EVENT_DISCONNECT ")
         ).on("realtime", args -> {
            if(listener!=null) listener.onMessage(args[0].toString());
        }).on("dataset:style_updated", args -> {
            if(listener!=null) listener.onMessage(args[0].toString());
        });
        socket.connect();
    }

    public void fetchWebsocketsSession() {
        com.amigocloud.AmigoRest client = new AmigoRest(apiToken);
        String result = client.get(baseURL+"/api/v1/me/start_websocket_session");
        JSONObject obj = null;
        try {
            obj = new JSONObject(result);
            websocket_token = obj.getString("websocket_session");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void fetchWebsocketsSessionRealTime() {
        AmigoRest client = new AmigoRest(apiToken);
        String result = client.get(baseURL+"/api/v1/users/"+userId+"/projects/"+projectId+"/datasets/"+datasetId+"/start_websocket_session");

        JSONObject obj = null;
        try {
            obj = new JSONObject(result);
            websocket_token = obj.getString("websocket_session");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
