#include <PS2X_lib.h>


  //for v1.6
/******************************************************************
   set pins connected to PS2 controller:
     - 1e column: original
     - 2e colmun: Stef?
   replace pin numbers by the ones you use
 ******************************************************************/
#define PS2_DAT        17
#define PS2_CMD        16
#define PS2_SEL        15
#define PS2_CLK        14
#define a1             23
#define a2             6
#define b1             25
#define b2             2
#define c1             27
#define c2             12
#define d1             29
#define d2             10
#define p1             22
#define p2             26  
int j;
int i=j=100;

/******************************************************************
   select modes of PS2 controller:
     - pressures = analog reading of push-butttons
     - rumble    = motor rumbling
   uncomment 1 of the lines for each mode selection
 ******************************************************************/
#define pressures   true
#define pressures   false
#define rumble      true
#define rumble      false

PS2X ps2x; // create PS2 Controller Class

//right now, the library does NOT support hot pluggable controllers, meaning
//you must always either restart your Arduino after you connect the controller,
//or call config_gamepad(pins) again after connecting the controller.

int error = 0;
byte type = 0;
byte vibrate = 0;

void setup() {

  Serial.begin(57600);
  pinMode(a1, OUTPUT);
  pinMode(a2, OUTPUT);
  pinMode(b1, OUTPUT);
  pinMode(b2, OUTPUT);
  pinMode(c1, OUTPUT);
  pinMode(c2, OUTPUT);
  pinMode(d1, OUTPUT);
  pinMode(d2, OUTPUT);
  delay(300);  //added delay to give wireless ps2 module some time to startup, before configuring it

  //CHANGES for v1.6 HERE!!! **************PAY ATTENTION*************

  //setup pins and settings: GamePad(clock, command, attention, data, Pressures?, Rumble?) check for error
  error = ps2x.config_gamepad(PS2_CLK, PS2_CMD, PS2_SEL, PS2_DAT, pressures, rumble);

  if (error == 0) {
    Serial.print("Found Controller, configured successful ");
    Serial.print("pressures = ");
    if (pressures)
      Serial.println("true ");
    else
      Serial.println("false");
    Serial.print("rumble = ");
    if (rumble)
      Serial.println("true)");
    else
      Serial.println("false");
    Serial.println("Try out all the buttons, X will vibrate the controller, faster as you press harder;");
    Serial.println("holding L1 or R1 will print out the analog stick values.");
    Serial.println("Note: Go to www.billporter.info for updates and to report bugs.");
  }
  else if (error == 1)
    Serial.println("No controller found, check wiring, see readme.txt to enable debug. visit www.billporter.info for troubleshooting tips");

  else if (error == 2)
    Serial.println("Controller found but not accepting commands. see readme.txt to enable debug. Visit www.billporter.info for troubleshooting tips");

  else if (error == 3)
    Serial.println("Controller refusing to enter Pressures mode, may not support it. ");

  //  Serial.print(ps2x.Analog(1), HEX);

  type = ps2x.readType();
  switch (type) {
    case 0:
      Serial.print("Unknown Controller type found ");
      break;
    case 1:
    
      Serial.print("DualShock Controller found ");
      break;
    case 2:
      Serial.print("GuitarHero Controller found ");
      break;
    case 3:
      Serial.print("Wireless Sony DualShock Controller found ");
      break;
  }
}

void loop() {
  /* You must Read Gamepad to get new values and set vibration values
     ps2x.read_gamepad(small motor on/off, larger motor strenght from 0-155)
     if you don't enable the rumble, use ps2x.read_gamepad(); with no values
     You should call this at least once a second
  */
  if (error == 1) //skip loop if no controller found
    return;

  if (type == 2) { //Guitar Hero Controller
    ps2x.read_gamepad();          //read controller

    if (ps2x.ButtonPressed(GREEN_FRET))
      Serial.println("Green Fret Pressed");
    if (ps2x.ButtonPressed(RED_FRET))
      Serial.println("Red Fret Pressed");
    if (ps2x.ButtonPressed(YELLOW_FRET))
      Serial.println("Yellow Fret Pressed");
    if (ps2x.ButtonPressed(BLUE_FRET))
      Serial.println("Blue Fret Pressed");
    if (ps2x.ButtonPressed(ORANGE_FRET))
      Serial.println("Orange Fret Pressed");

    if (ps2x.ButtonPressed(STAR_POWER))
      Serial.println("Star Power Command");

    if (ps2x.Button(UP_STRUM))         //will be TRUE as long as button is pressed
      Serial.println("Up Strum");
    if (ps2x.Button(DOWN_STRUM))
      Serial.println("DOWN Strum");

    if (ps2x.Button(PSB_START))        //will be TRUE as long as button is pressed
      Serial.println("Start is being held");
    if (ps2x.Button(PSB_SELECT))
      Serial.println("Select is being held");

    if (ps2x.Button(ORANGE_FRET)) {    // print stick value IF TRUE
      Serial.print("Wammy Bar Position:");
      Serial.println(ps2x.Analog(WHAMMY_BAR), DEC);
    }
  }
  else { //DualShock Controller
    ps2x.read_gamepad(false, vibrate); //read controller and set large motor to spin at 'vibrate' speed

    int  xn = map(ps2x.Analog(PSS_LX), 0, 127, -127, 0);
         Serial.print(xn);
    int  xp = map(ps2x.Analog(PSS_LX), 128, 255, 0, 127);

    int  yn = map(ps2x.Analog(PSS_LY), 128, 255, 0, -127);
    int  yp = map(ps2x.Analog(PSS_LY), 0, 127, 127, 0);

    int  xn1 = map(ps2x.Analog(PSS_RX), 0, 127, -127, 0);
    int  xp1 = map(ps2x.Analog(PSS_RX), 128, 255, 0, 127);

    int  yn1 = map(ps2x.Analog(PSS_RY), 128, 255, 0, -127);
    int  yp1 = map(ps2x.Analog(PSS_RY), 0, 127, 127, 0);



  if (yp < 90 && yn >= -90 && xp <= 90 && xn >= -90 && yp1 < 90 && yn1 >= -90 && xp1 <= 90 && xn1 >= -90)
    {
      //Serial.println("L Stop");
      analogWrite(a1, 0);
      analogWrite(a2, 0);
      analogWrite(b1, 0);
      analogWrite(b2, 0);
      analogWrite(c1, 0);
      analogWrite(c2, 0);
      analogWrite(d1, 0);
      analogWrite(d2, 0);

    }
    
    if (yp > 90 && yn >= -90 && xp <= 90 && xn >= -90)
    {
      Serial.println("L UP");
      digitalWrite(a1, HIGH);
      analogWrite(a2, i);
      digitalWrite(b1, LOW);
      analogWrite(b2, i);
      digitalWrite(c1, LOW);
      analogWrite(c2, i);
      digitalWrite(d1, LOW);
      analogWrite(d2, i);;

    }

    if (yp <= 90 && yn < -90 && xp <= 90 && xn >= -90)
    {
      Serial.println("L DOWN");
      digitalWrite(a1, LOW);
      analogWrite(a2, i);
      digitalWrite(b1, HIGH);
      analogWrite(b2, i);
      digitalWrite(c1, HIGH);
      analogWrite(c2, i);
      digitalWrite(d1, HIGH);
      analogWrite(d2, i);
    }
    if (yp <= 90 && yn >= -90 && xp > 90 && xn >= -90)
    {
      Serial.println("L right");
     digitalWrite(a1, LOW);
      analogWrite(a2, i);
      digitalWrite(b1, LOW);
      analogWrite(b2, i);
      digitalWrite(c1, HIGH);
      analogWrite(c2, i);
      digitalWrite(d1, LOW);
      analogWrite(d2, i);
}

    if (yp <= 90 && yn >= -90 && xp <= 90 && xn < -90)
    {
      Serial.println("L left");
      digitalWrite(a1, HIGH);
      analogWrite(a2, i);
      digitalWrite(b1, HIGH);
      analogWrite(b2, i);
      digitalWrite(c1, LOW);
      analogWrite(c2, i);
      digitalWrite(d1, HIGH);
      analogWrite(d2, i);

    }


//right stick

  /* if ()
    {
      Serial.println("R Stop");
      analogWrite(a1, 0);
      analogWrite(a2, 0);
      analogWrite(b1, 0);
      analogWrite(b2, 0);
      analogWrite(c1, 0);
      analogWrite(c2, 0);
      analogWrite(d1, 0);
      analogWrite(d2, 0);

    }*/
    
    if (yp1 > 90 && yn1 >= -90 && xp1 <= 90 && xn1 >= -90)
    {
      Serial.println("R UP");
      digitalWrite(b1, LOW);
      analogWrite(b2, i);
      digitalWrite(d1, LOW);
      analogWrite(d2, i);
    }

    if (yp1 <= 90 && yn1 < -90 && xp1 <= 90 && xn1 >= -90)
    {
      Serial.println("R DOWN");
      digitalWrite(b1, HIGH);
      analogWrite(b2, i);
      digitalWrite(d1, HIGH);
      analogWrite(d2, i);
      }
    if (yp1 <= 90 && yn1 >= -90 && xp1 > 90 && xn1 >= -90)
    {
      Serial.println("R right CLOCK");
       digitalWrite(a1, LOW);
      analogWrite(a2, i);
      digitalWrite(c1, HIGH);
      analogWrite(c2,i); 
      }

    if (yp1 <= 90 && yn1 >= -90 && xp1 <= 90 && xn1 < -90)
    {
      Serial.println("R left ANTI CLOCK");
      digitalWrite(a1, HIGH);
      analogWrite(a2, i);
      digitalWrite(c1, LOW);
      analogWrite(c2, i);
     }












    if (ps2x.Button(PSB_START))        //will be TRUE as long as button is pressed
      Serial.println("Start is being held");
    if (ps2x.Button(PSB_SELECT))
      Serial.println("Select is being held");

    if (ps2x.Button(PSB_PAD_UP)) {     //will be TRUE as long as button is pressed

      Serial.print("Up held this hard: ");
      Serial.println(ps2x.Analog(PSAB_PAD_UP), DEC);
    }
    if (ps2x.Button(PSB_PAD_RIGHT)) {
      Serial.print("Right held this hard: ");
      Serial.println(ps2x.Analog(PSAB_PAD_RIGHT), DEC);
    }
    if (ps2x.Button(PSB_PAD_LEFT)) {
      Serial.print("LEFT held this hard: ");
      Serial.println(ps2x.Analog(PSAB_PAD_LEFT), DEC);
    }
    if (ps2x.Button(PSB_PAD_DOWN)) {

      Serial.print("DOWN held this hard: ");
      Serial.println(ps2x.Analog(PSAB_PAD_DOWN), DEC);
    }
    if (ps2x.ButtonPressed(PSB_CROSS))  {           //will be TRUE if button was JUST pressed OR released
       
        i-=50;
       //i-=5; 
       Serial.println("X just pressed");
    }
    if (ps2x.ButtonPressed(PSB_TRIANGLE)){
        i+=50;
       //i+=5;  
         
      Serial.println("Triangle just pressed");
      }
    
    if (ps2x.Button(PSB_L1)) { //|| ps2x.Button(PSB_R1)) { //print stick values if either is TRUE
      Serial.println("L1 Pressed");
      digitalWrite(a1, LOW);
      analogWrite(a2, i);
      digitalWrite(b1, LOW);
      analogWrite(b2, i);
      digitalWrite(c1, LOW);
      analogWrite(c2, i);
      digitalWrite(d1, HIGH);
      analogWrite(d2, i);
      }
     if (ps2x.Button(PSB_R1)) { //|| ps2x.Button(PSB_R1)) { //print stick values if either is TRUE
      Serial.println("R1 Pressed");
      digitalWrite(a1, HIGH);
      analogWrite(a2, i);
      digitalWrite(b1, HIGH);
      analogWrite(b2, i);
      digitalWrite(c1, HIGH);
      analogWrite(c2, i);
      digitalWrite(d1, LOW);
      analogWrite(d2, i);
      }

    vibrate = ps2x.Analog(PSAB_CROSS);  //this will set the large motor vibrate speed based on how hard you press the blue (X) button
    if (ps2x.NewButtonState()) {        //will be TRUE if any button changes state (on to off, or off to on)
      if (ps2x.Button(PSB_L3))
        Serial.println("L3 pressed");
      if (ps2x.Button(PSB_R3))
        Serial.println("R3 pressed");
      if (ps2x.Button(PSB_L2)) {
        
        Serial.println("dig left dw");
      }
      if (ps2x.Button(PSB_R2)) {
        Serial.println("dig right dw");
      }
      
        
    }

    if (ps2x.ButtonPressed(PSB_CIRCLE)) { //will be TRUE if button was JUST pressed
     
      Serial.println("Circle just pressed");
    }
    
    if (ps2x.ButtonReleased(PSB_CIRCLE)) { //will be TRUE if button was JUST pressed
      analogWrite(a1, 0);
      analogWrite(a2, 0);
      analogWrite(b1, 0);
      analogWrite(b2, 0);
      analogWrite(c1, 0);
      analogWrite(c2, 0);
      analogWrite(d1, 0);
      analogWrite(d2, 0);

      Serial.println("Circle just pressed");
    }
    
    if (ps2x.ButtonPressed(PSB_SQUARE)) {            //will be TRUE if button was JUST released
        Serial.println("Square just pressed");
    }
    if (ps2x.ButtonReleased(PSB_SQUARE)) {            //will be TRUE if button was JUST released
      analogWrite(a1, 0);
      analogWrite(a2, 0);
      analogWrite(b1, 0);
      analogWrite(b2, 0);
      analogWrite(c1, 0);
      analogWrite(c2, 0);
      analogWrite(d1, 0);
      analogWrite(d2, 0);
      Serial.println("Square just released");
    }
    if (ps2x.ButtonPressed(PSB_L1)) { //|| ps2x.Button(PSB_R1)) { //print stick values if either is TRUE
      Serial.println("L1 Pressed");
      digitalWrite(p1,HIGH);
      }
      if (ps2x.ButtonReleased(PSB_L1)) { //|| ps2x.Button(PSB_R1)) { //print stick values if either is TRUE
      Serial.println("L1 released");
      digitalWrite(p1,LOW);
      }

    if (ps2x.ButtonPressed(PSB_R1)) { //|| ps2x.Button(PSB_R1)) { //print stick values if either is TRUE
      Serial.println("R1 Pressed");
    digitalWrite(p2,HIGH);
    
    }
  
    if (ps2x.ButtonReleased(PSB_R1)) { //|| ps2x.Button(PSB_R1)) { //print stick values if either is TRUE
      Serial.println("R1 released");
    digitalWrite(p2,LOW);
    
    }
  
  }
  delay(10);
}
