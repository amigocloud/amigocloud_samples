package com.amigocloud.amigomobile.locator;

import android.app.Application;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class LocatorApplication extends Application {

	private static ExecutorService networkThreadPool = Executors.newFixedThreadPool(2);

	private static AmigoRest restClient;

	@Override
	public void onCreate() {
		super.onCreate();
		restClient = new AmigoRest();
	}

	public static void runOnNetworkThread(Runnable r) {
		networkThreadPool.execute(r);
	}

	public static AmigoRest getRestClient() {
		return restClient;
	}


}
