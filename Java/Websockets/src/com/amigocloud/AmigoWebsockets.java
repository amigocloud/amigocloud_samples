package com.amigocloud;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.drafts.Draft_10;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.util.Random;

/*
 * Credits to the websockets library: https://github.com/TooTallNate/Java-WebSocket
 */
public class AmigoWebsockets {

    private WebSocketClient mWs=null;
    private String websocket_token="";
    private String userID = "";
    private String projectID = "";
    private String datasetID = "";

    private boolean connected=false;
    private boolean realtime=false;

    private AmigoWebsocketListener listener=null;

    private static final String BASE_URL = "www.amigocloud.com";
    private static final String END_POINT= "/amigosocket";

    public AmigoWebsockets(long userID, String apiToken, AmigoWebsocketListener listener) {
        this.userID = Long.toString(userID);
        this.listener = listener;
        AmigoRest client = new AmigoRest(apiToken);
        String result = client.get("https://"+BASE_URL+"/api/v1/me/start_websocket_session");
        JSONObject obj = null;
        try {
            obj = new JSONObject(result);
            websocket_token = obj.getString("websocket_session");
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public AmigoWebsockets(long userID, long projectID, long datasetID, String apiToken, AmigoWebsocketListener listener) {
        this.userID = Long.toString(userID);
        this.projectID = Long.toString(projectID);
        this.datasetID = Long.toString(datasetID);
        this.listener = listener;

        realtime = true;

        AmigoRest client = new AmigoRest(apiToken);
        String uri = "https://"+BASE_URL+"/api/v1/users/"+userID+"/projects/"+projectID+"/datasets/"+datasetID+"/start_websocket_session";

        String result = client.get(uri);
        JSONObject obj = null;
        try {
            obj = new JSONObject(result);
            websocket_token = obj.getString("websocket_session");
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public boolean isConnected () {return connected;}

    public boolean connect() {
        if(websocket_token.length()==0)
            return false;

        try {
            String uri = "ws://"+BASE_URL+":5005/socket.io/1/websocket/";
            Random rand = new Random();
            uri += Long.toString(rand.nextLong());

            mWs = new WebSocketClient(new URI(uri), new Draft_10()) {
                @Override
                public void onMessage(String message) {
                    parseMessage(message);
                }

                @Override
                public void onOpen(ServerHandshake handshake) {
                    System.out.println("Opened websockets connection");
                }

                @Override
                public void onClose(int code, String reason, boolean remote) {
                    System.out.println("closed connection, remote:"+remote+", code(" + Integer.toString(code) + "), reason: " + reason);
                }

                @Override
                public void onError(Exception ex) {
                    ex.printStackTrace();
                }

            };

            //open websocket
            mWs.connect();

            // Wait for connection
            int counter=100;
            while (!isConnected() && counter > 0){
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                counter--;
            }

           if(counter > 1) {
               return emit();
           }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public boolean emit()
    {
        String emitargs;
        if(realtime) {
            emitargs = "{\"userid\":" + userID + ",\"datasetid\":"+datasetID+",\"websocket_session\":\"" + websocket_token + "\"}";
        } else {
            emitargs = "{\"userid\":" + userID + ",\"websocket_session\":\"" + websocket_token + "\"}";
        }
        String msg = "{\"name\":\"authenticate\",\"args\":["+emitargs+"]}";
        send(5, msg);
        return true;
    }

    public void send(int type, String msg) {
        String message;
        message = Integer.toString(type) + "::" + END_POINT + ":" + msg;
        mWs.send(message);
    }

    public void parseMessage(String message) {
        String[] msg = message.split("::");
        if(msg.length == 0)
            return;
        if(msg[0].contentEquals("1") )
        {
            if(msg.length==1) {
                send(1, ""); // Emit reply
            } else {
                connected = true;
            }
            return;
        }
        if(msg[0].contentEquals("5") && msg.length>1) {
            String msg5 = msg[1].replace(END_POINT+":","");;
            if(listener!=null) {
                listener.onMessage(msg5);
            }
        }

        if(msg[0].contentEquals("2")) {
            System.out.println("Keep alive message: " + message);
        }

    }
}
