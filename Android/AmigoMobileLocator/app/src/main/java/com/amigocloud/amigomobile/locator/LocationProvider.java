package com.amigocloud.amigomobile.locator;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.provider.Settings;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class LocationProvider implements android.location.LocationListener {
	private final Context mContext;

	private boolean hasData = false;
	private Location location;
	private double lat;
	private double lng;
	private double altitude;
	private double bearing;
	private double accuracy;
    private double speed;
	private int numSatellites;

	private boolean gpsEnabled;
	private boolean networkEnabled;
	private boolean running;

	private static final int UPDATE_MSG = 0;
	private static final long MIN_DISTANCE_CHANGE_FOR_UPDATES = 0;
	private static final long MIN_TIME_GPS_UPDATES = 500;
	private static final long MIN_TIME_NETWORK_UPDATES = 1000 * 5;

	private String deviceId;
	private long userId;
	private long projectId;
	private long datasetId;

	private long numSucceded;
	private long numFailed;

	public long getNumFailed() { return numFailed; }
	public long getNumSucceded() { return numSucceded; }

	protected LocationManager locationManager;

	private List<LocationListener> listeners = new CopyOnWriteArrayList<LocationListener>();

	private Handler handler = new Handler() {
		@Override
		public void handleMessage(Message msg) {
			super.handleMessage(msg);
			if(msg.what == UPDATE_MSG) {
				updateLocation();
			}
		}
	};

	public LocationProvider(Context context) {
		this.mContext = context;
	}

	private void updateData(Location location) {
		this.location = location;
		lat = location.getLatitude();
		lng = location.getLongitude();
		if(location.hasAltitude())
			altitude = location.getAltitude();
		else
			altitude = 0;
		if(location.hasBearing())
			bearing = location.getBearing();
		else
			bearing = 0;
		if(location.hasAccuracy())
			accuracy = location.getAccuracy();
		else
			accuracy = 0;
		if(location.hasSpeed())
			speed = getSpeed();
		else
			speed = 0;

		this.hasData = true;

		final String xml = getMoovboxXML();
		LocatorApplication.runOnNetworkThread(new Runnable() {
			@Override
			public void run() {
				if(LocatorApplication.getRestClient().sendLocation(userId, projectId, datasetId, xml))
					numSucceded++;
				else
					numFailed++;
			}
		});

		for(LocationListener l : listeners) {
			l.onLocation(location);
		}
	}

	private synchronized void updateLocation() {
		if(!running)
			return;
		try {
			locationManager = (LocationManager) mContext.getSystemService(Context.LOCATION_SERVICE);
			if(locationManager != null) {
				boolean isGPSEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);
				boolean isNetworkEnabled = locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER);

				if ((isGPSEnabled && !gpsEnabled) || (!isGPSEnabled && isNetworkEnabled && !networkEnabled)) {
					locationManager.removeUpdates(this);
					if (isGPSEnabled) {
						locationManager.requestLocationUpdates(
								LocationManager.GPS_PROVIDER,
								MIN_TIME_GPS_UPDATES,
								MIN_DISTANCE_CHANGE_FOR_UPDATES, this);
						gpsEnabled = true;
						networkEnabled = false;
					} else {
						locationManager.requestLocationUpdates(
								LocationManager.NETWORK_PROVIDER,
								MIN_TIME_NETWORK_UPDATES,
								MIN_DISTANCE_CHANGE_FOR_UPDATES, this);
						networkEnabled = true;
						gpsEnabled = false;
					}
				} else if (!isGPSEnabled && !isNetworkEnabled) {
					hasData = false;
					gpsEnabled = false;
					networkEnabled = false;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		handler.sendEmptyMessageDelayed(UPDATE_MSG, 1000 * 30);
	}

	public synchronized void stop() {
		running = false;
		if(locationManager != null){
			locationManager.removeUpdates(this);
		}
		handler.removeMessages(UPDATE_MSG);
		gpsEnabled = false;
		networkEnabled = false;
	}

	public synchronized void start(String deviceId, long userId, long projectId, long datasetId){
		numSucceded = 0;
		numFailed = 0;

		this.deviceId = deviceId;
		this.userId = userId;
		this.projectId = projectId;
		this.datasetId = datasetId;

		stop();
		running = true;
		updateLocation();
	}

	public Location getLocation() {
		return location;
	}

	public double getLat(){
		return lat;
	}

	public double getLng(){
		return lng;
	}

	public double getAltitude() {
		return altitude;
	}

	public double getBearing() {
		return bearing;
	}

	public double getAccuracy() {
		return accuracy;
	}

    public double getSpeed() {
        return speed;
    }

	public double getNumSatellites() {
		return numSatellites;
	}

    public boolean hasData() {
		return this.hasData;
	}

	@Override
	public void onLocationChanged(Location location) {
		updateData(location);
	}

	@Override
	public void onProviderEnabled(String s) {
		updateLocation();
	}

	@Override
	public void onProviderDisabled(String s) {
		updateLocation();
	}

	@Override
	public void onStatusChanged(String s, int i, Bundle bundle) {
		if(bundle != null) {
			numSatellites = bundle.getInt("satellites", 0);
		}
	}

	public void addListener(LocationListener l) {
		listeners.add(l);
	}

	public void removeListener(LocationListener l) {
		listeners.remove(l);
	}

	private String getMoovboxXML() {
		long timestamp = System.currentTimeMillis() / 1000L;
		StringBuilder builder = new StringBuilder();
		builder.append("<gps id=\"").append(deviceId).append("\">");
		builder.append("<coordinates>");
		builder.append("<coordinate>");

		builder.append("<time>");
		builder.append(timestamp);
		builder.append("</time>");

		builder.append("<latitude>");
		builder.append(lng);
		builder.append("</latitude>");

		builder.append("<longitude>");
		builder.append(lat);
		builder.append("</longitude>");

		builder.append("<altitude>");
		builder.append(altitude);
		builder.append("</altitude>");

		builder.append("<speed>");
		builder.append(speed);
		builder.append("</speed>");

		builder.append("<bearing>");
		builder.append(bearing);
		builder.append("</bearing>");

		builder.append("<horizontal_accuracy>");
		builder.append(accuracy);
		builder.append("</horizontal_accuracy>");

		builder.append("<satellites>");
		builder.append(numSatellites);
		builder.append("</satellites>");

		builder.append("</coordinate>");
		builder.append("</coordinates>");
		builder.append("</gps>");
		return builder.toString();
	}

	public static void showSettingsAlert(final Context context){
		LocationManager locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
		if(locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
			return;
		}
		AlertDialog.Builder alertDialog = new AlertDialog.Builder(context);

		// Setting Dialog Title
		alertDialog.setTitle("GPS is Disabled");

		// On pressing Settings button
		alertDialog.setPositiveButton("Settings", new DialogInterface.OnClickListener() {
			public void onClick(DialogInterface dialog,int which) {
				Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
				context.startActivity(intent);
			}
		});

		// on pressing cancel button
		alertDialog.setNegativeButton("Ignore", new DialogInterface.OnClickListener() {
			public void onClick(DialogInterface dialog, int which) {
				dialog.cancel();
			}
		});

		// Showing Alert Message
		alertDialog.show();
	}
}
