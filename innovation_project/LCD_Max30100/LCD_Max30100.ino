/*
Arduino-MAX30100 oximetry / heart rate integrated sensor library
Copyright (C) 2016  OXullo Intersecans <x@brainrapers.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// This example must be used in conjunction with the Processing sketch located
// in extras/rolling_graph
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000

// PulseOximeter is the higher level interface to the sensor
// it offers:
//  * beat detection reporting
//  * heart rate calculation
//  * SpO2 (oxidation level) calculation
PulseOximeter pox;

uint32_t tsLastReport = 0;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
//    Serial.println("B:1");
}

void setup()
{
    Serial.begin(115200);
    lcd.begin(16, 2);

    // Initialize the PulseOximeter instance and register a beat-detected callback
    // The parameter passed to the begin() method changes the samples flow that
    // the library spews to the serial.
    // Options:
    //  * PULSEOXIMETER_DEBUGGINGMODE_PULSEDETECT : filtered samples and beat detection threshold
    //  * PULSEOXIMETER_DEBUGGINGMODE_RAW_VALUES : sampled values coming from the sensor, with no processing
    //  * PULSEOXIMETER_DEBUGGINGMODE_AC_VALUES : sampled values after the DC removal filter

    // Initialize the PulseOximeter instance
    // Failures are generally due to an improper I2C wiring, missing power supply
    // or wrong target chip
    if (!pox.begin()) {
        Serial.println("ERROR: Failed to initialize pulse oximeter");
        lcd.print("ERROR: FAILED TO INITIALIZE PULSE OXIMETER");
        for(;;);
    }

   
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop()
{
    // Make sure to call update as fast as possible
    pox.update();
    
    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        float bpm=pox.getHeartRate();
        float SpO2=pox.getSpO2();

        if (SpO2 > 100) {
          SpO2/=10;
        }
        
        if ((bpm == 0) || (SpO2 == 0)) {
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("PUT FINGER");
        }
        else {
        lcd.clear();
        Serial.print("H:");
        Serial.println(bpm);
        lcd.setCursor(0, 0); 
        if (SpO2 < 95.) {
          lcd.print("EMERGENCY ");
        } 
        lcd.print("BPM   ");
        lcd.print(bpm);
        Serial.print("O:");
        Serial.println(SpO2);
        lcd.setCursor(0, 1);
        lcd.print("SPO2  ");
        lcd.print(SpO2);

        }
        tsLastReport = millis();
        
    }
}
