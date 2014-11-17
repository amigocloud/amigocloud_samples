package com.amigocloud.amigomobile.locator;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class LocationService extends Service {

    private static LocationProvider provider;

	private static boolean isRunning;

	private static String deviceId;
	private static long userId;
	private static long projectId;
	private static long datasetId;

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        provider = new LocationProvider(this);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
		isRunning = true;
        provider.start(deviceId, userId, projectId, datasetId);
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        provider.stop();
		isRunning = false;
    }

	public static void setIds(String devId, long uId, long pId, long dId) {
		deviceId = devId;
		userId = uId;
		projectId = pId;
		datasetId = dId;
	}

	public static boolean isRunnning() { return isRunning; }

	public static long getNumFailed() {
		if(provider == null)
			return 0;
		return provider.getNumFailed();
	}

	public static long getNumSucceded() {
		if(provider == null)
			return 0;
		return provider.getNumSucceded();
	}
}
