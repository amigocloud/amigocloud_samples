package com.amigocloud;

public interface AmigoWebsocketListener {
    public void onMessage(String message);

    /**
     * Called by WebSocketClient.onClose() to indicate connection closed and
     * there is a problem.
     *
     * @param code
     * @param reason
     */
    public void onClose(int code, String reason);
}
