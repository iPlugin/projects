#define sensorHumidity_pin A0
#define sensorLight_pin A1
#define watering_can_pin 2

int sensorLight_value = 0;
int sensorHumidity_value = 0;

unsigned long last_fix_time = 0;
unsigned long next_check = 5000;

void printInfo(int value, float voltage, int percentages, String sensor) {
  Serial.print(sensor);
  Serial.print(" - Analog value: ");
  Serial.print(value);
  Serial.print("\t Vol: ");
  Serial.print(voltage, 2);
  Serial.print("V\t Perc: ");
  Serial.print(percentages);
  Serial.println("%");
}

int getLight() {
  sensorLight_value = analogRead(sensorLight_pin);
  float sensorLight_vol = sensorLight_value * (5.0 / 1023.0);
  int sensorLight_percentages = map(sensorLight_value, 0, 1023, 100, 0);
  printInfo(sensorLight_value, sensorLight_vol, sensorLight_percentages, "Light");
  return sensorLight_percentages;
}

int getHumidity() {
  sensorHumidity_value = analogRead(sensorHumidity_pin);
  float sensorHumidity_vol = sensorHumidity_value * (5.0 / 1023.0);
  int sensorHumidity_percentages = map(sensorHumidity_value, 0, 1023, 100, 0);
  printInfo(sensorHumidity_value, sensorHumidity_vol, sensorHumidity_percentages, "Humidity");
  return sensorHumidity_percentages;
}

void setup() {
  pinMode(sensorLight_pin, INPUT);
  pinMode(sensorHumidity_pin, INPUT);
  pinMode(watering_can_pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (millis() - last_fix_time > next_check) {
    last_fix_time = millis();
  
    Serial.println("----------------------------------------------------------");

    int lightPercentages = getLight();
    int humidityPercentages = getHumidity();

    if (lightPercentages >= 40 && humidityPercentages < 60) {
      Serial.println("Watering system: ON");
      digitalWrite(watering_can_pin, HIGH);
    } else {
      Serial.println("Watering system: OFF");
      digitalWrite(watering_can_pin, LOW);
    }
  }
}
