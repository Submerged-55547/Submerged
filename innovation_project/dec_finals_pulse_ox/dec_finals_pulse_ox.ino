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


#include <Wire.h>

#include "MAX30100_PulseOximeter.h"

#include "Adafruit_Sensor.h"

#include "DHT.h"

// Pin assignments
// Analog
#define ADC_PIN 0

//Digital
#define WARNING_LED_PIN A3
#define BUTTON_PIN 1
#define BUZZER_PIN 2
#define DIRA_MOTOR_PIN 3
#define DIRB_MOTOR_PIN 4
#define ENABLE_MOTOR_PIN 5
#define DHT_PIN 6
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
#define EMERGENCY_LED_PIN 13

// Set DHT type, uncomment whatever type you're using!
#define DHTTYPE DHT11 // DHT 11 

// Initialize DHT sensor for normal 16mhz Arduino:
DHT dht = DHT(DHT_PIN, DHTTYPE);

#define REPORTING_PERIOD_MS 1000

// PulseOximeter is the higher level interface to the sensor
// it offers:
//  * beat detection reporting
//  * heart rate calculation
//  * SpO2 (oxidation level) calculation
PulseOximeter pox;

uint32_t tsLastReport = 0;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected() {}

void setup() {
    // Digital output pins
    pinMode(EMERGENCY_LED_PIN, OUTPUT);
    pinMode(WARNING_LED_PIN, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(ENABLE_MOTOR_PIN, OUTPUT);
    pinMode(DIRA_MOTOR_PIN, OUTPUT);
    pinMode(DIRB_MOTOR_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    Serial.println("AAA LOW");
    analogWrite(WARNING_LED_PIN, 0);

    // Digital input pin
    pinMode(BUTTON_PIN, INPUT);

    // Serial communication to computer for debugging
    Serial.begin(115200);

    // initialize LCD
    lcd.begin(16, 2);
    lcd.setCursor(0, 1);

    DHT dht = DHT(DHT_PIN, DHTTYPE);

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
        lcd.print("ERROR Failed to initialize");
        for (;;);
    }

    pox.setOnBeatDetectedCallback(onBeatDetected);
}

int temperature;
int motor_time = 0;
int emergency_start = 0;

void loop() {
    int i;
    // Make sure to call update as fast as possible
    pox.update();

    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"]
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {

        Serial.println("Reading");
        int bpm = (int) pox.getHeartRate();
        float SpO2 = pox.getSpO2();
        if (SpO2 > 100) {
            SpO2 /= 10;
        }

        // read the state of the pushbutton value:
        int emergencyButtonState = digitalRead(BUTTON_PIN);
        if (emergencyButtonState == LOW) {
            // Panic button was pressed
            emergency_start = 5;
        }
        lcd.clear();
        if ((bpm == 0) || (SpO2 == 0)) {
            Serial.print("Wear wetsuit");
            lcd.setCursor(0, 0);
            lcd.print("Wear wetsuit");
        } else {
            lcd.setCursor(0, 0);
            lcd.print("BPM:");
            lcd.print(bpm);
            lcd.setCursor(7, 0);
            lcd.print(" SPO2:");
            lcd.print(pox.getSpO2());
            if (SpO2 < 96) {
                emergency_start++;
            } else {
                // Reset back to no emergency
                emergency_start = 0;
                digitalWrite(EMERGENCY_LED_PIN, LOW);
                digitalWrite(ENABLE_MOTOR_PIN, LOW);
            }

        }

        if (emergency_start > 0) {
            // Sound buzzer and emergency led
            digitalWrite(EMERGENCY_LED_PIN, HIGH);
            digitalWrite(BUZZER_PIN, HIGH);
            delay(10);
            digitalWrite(BUZZER_PIN, LOW);

            emergency_start++;
            if (emergency_start > 5) {
                // Activate tether
                digitalWrite(ENABLE_MOTOR_PIN, HIGH);
                digitalWrite(DIRA_MOTOR_PIN, HIGH);
                digitalWrite(DIRB_MOTOR_PIN, LOW);

                motor_time++;
            }
        }
        if (motor_time > 10) {
            digitalWrite(ENABLE_MOTOR_PIN, LOW);
        }
        // Read temperature  
        float f = dht.readTemperature(true);
        if (!isnan(f)) {
            temperature = (int) f;
        }
        lcd.setCursor(0, 1);
        lcd.print("T:");
        lcd.print(temperature);
        tsLastReport = millis();

        // Read depth
        int depth = analogRead(ADC_PIN); //get adc value
        lcd.setCursor(8, 1);
        lcd.print(" D:");
        lcd.print(depth);

        if ((depth > 200) || (temperature > 110) || (temperature < -20)) {
            // Sound buzzer and turn on warning LED
            Serial.println("WARNING");
            Serial.println("AAA HIGH");
            digitalWrite(LED_BUILTIN, HIGH);
            analogWrite(WARNING_LED_PIN, 255);
            digitalWrite(BUZZER_PIN, HIGH);
            delay(10);
            digitalWrite(BUZZER_PIN, LOW);
        } else {
            Serial.println("AAA2 LOW");
            analogWrite(WARNING_LED_PIN, 0);
            digitalWrite(LED_BUILTIN, LOW);

        }

    }
}
