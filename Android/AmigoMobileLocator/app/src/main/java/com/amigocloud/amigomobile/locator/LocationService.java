package com.amigocloud.amigomobile.locator;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class LocationService extends Service {

    private LocationProvider provider;

	private static boolean isRunning;

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
        provider.start(userId, projectId, datasetId);
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        provider.stop();
		isRunning = false;
    }

	public static void setIds(long uId, long pId, long dId) {
		userId = uId;
		projectId = pId;
		datasetId = dId;
	}

	public static boolean isRunnning() { return isRunning; }
}
