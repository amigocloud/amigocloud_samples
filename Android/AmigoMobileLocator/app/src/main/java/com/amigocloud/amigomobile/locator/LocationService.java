package com.amigocloud.amigomobile.locator;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class LocationService extends Service {

    private LocationProvider provider;

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
        provider.start();
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        provider.stop();
    }
}
