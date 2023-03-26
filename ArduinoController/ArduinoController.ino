const int DIST_TRIG_PIN = 6; // distance sensor trigger pin
const int DIST_ECHO_PIN = 7; // distance sensor echo pin
const int MOTOR_AIN1 = 13;   // control pin 1 on the motor driver for the right motor
const int MOTOR_AIN2 = 12;   // control pin 2 on the motor driver for the right motor
const int MOTOR_PWMA = 11;   // speed control pin on the motor driver for the right motor
const int RED_LED = 5;       // Active Scan Indicator LED
const int YELLOW_LED = 4;    // Ready Indicator LED
const int GREEN_LED = 3;     // Idle Indicator LED

enum SIGNAL
{
  UNDEF,
  READY,
  CLOCKWISE,
  COUNTER_CLOCKWISE,
};

int cycles = 0;
bool active = false;
SIGNAL selectedDirection = CLOCKWISE;

void setup()
{
  Serial.begin(9600);

  pinMode(DIST_TRIG_PIN, OUTPUT);
  pinMode(DIST_ECHO_PIN, INPUT);

  pinMode(MOTOR_AIN1, OUTPUT);
  pinMode(MOTOR_AIN2, OUTPUT);
  pinMode(MOTOR_PWMA, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  digitalWrite(GREEN_LED, HIGH);

  delay(30);
}

void loop()
{
  if (Serial.available() > 0)
  {
    int signal = Serial.parseInt();
    if (signal == READY)
    {
      digitalWrite(GREEN_LED, LOW);
      digitalWrite(YELLOW_LED, HIGH);
    }
    if ((signal == CLOCKWISE || signal == COUNTER_CLOCKWISE) && !active)
    {
      digitalWrite(YELLOW_LED, LOW);
      digitalWrite(RED_LED, HIGH);
      cycles = 0;
      active = true;
      selectedDirection = signal == CLOCKWISE ? CLOCKWISE : COUNTER_CLOCKWISE;
    }
  }

  if (active)
  {
    getRoomData();
  }

  cycles++;
  delay(34); // ms between readings
}

void getRoomData()
{
  if (cycles < 722) // 1 point of overlap
  {
    spinMotor(selectedDirection);
    Serial.println(getDistance());
  }
  else
  {
    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
    stopMotor();
    active = false;
  }
}

float getDistance()
{
  digitalWrite(DIST_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(DIST_TRIG_PIN, LOW);

  float echoTime = pulseIn(DIST_ECHO_PIN, HIGH);

  float calculatedDistance = echoTime / 58.2; // cm conversion

  return calculatedDistance;
}

void spinMotor(SIGNAL dir)
{
  float motorSpeed = 170;

  // Set Motor Direction
  if (dir == CLOCKWISE)
  {
    digitalWrite(MOTOR_AIN1, HIGH);
    digitalWrite(MOTOR_AIN2, LOW);
  }
  else // counterclockwise
  {
    digitalWrite(MOTOR_AIN1, LOW);
    digitalWrite(MOTOR_AIN2, HIGH);
  }
  // Apply Motor Power
  analogWrite(MOTOR_PWMA, abs(motorSpeed));
}

void stopMotor()
{
  digitalWrite(MOTOR_AIN1, LOW);
  digitalWrite(MOTOR_AIN2, LOW);
}
