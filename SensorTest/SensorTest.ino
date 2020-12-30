#include <OSR.h>

float window_s = 5;
float thresh = 0.5;
float check_hz = 10;

float key = 0;  // 0 is good typing, 1 is pecking

void print_arr(uint16_t arr[], float arrlen)
{
  for(uint8_t i = 0; i < arrlen; i++)
  {
    Serial.print(arr[i]);
    Serial.print(",");
  }
  Serial.print(key);
  Serial.println();
}

uint16_t gen_key_hex()
{
  uint16_t fsum = 1 * digitalRead(0) + 2 * digitalRead(1)+ 4 * digitalRead(2) + 8 * digitalRead(3);
  return fsum;
}

void setup()
{
  // put your setup code here, to run once:
  pinMode(0, INPUT);
  pinMode(1, INPUT);
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  Serial.begin(250000);
}

void loop() 
{
  float stepinc = 1 / (check_hz * window_s);
  float badpercent = 0;

  int winlen = window_s * check_hz;
  uint16_t winvals[winlen] = {0};
  int windex = 0;
  bool logging = false;

  float tstep = 1000 / check_hz;
  float tnext = millis() + tstep;
  while(true)
  {
    while(millis() < tnext);
    tnext += tstep;
    uint16_t fsum = digitalRead(0) + digitalRead(1)+ digitalRead(2) + digitalRead(3);
    if(fsum > 0)
    {
      if(fsum > 1)
        badpercent = 0;
//        badpercent -= (fsum - 1) * stepinc;
      else
        badpercent += stepinc;
      badpercent = badpercent < 0 ? 0 : badpercent;
      badpercent = badpercent > 1 ? 1 : badpercent;
    }

    winvals[windex] = gen_key_hex();
    windex += 1;

    if((windex >= winlen) && (logging == false))
      logging = true;

    if(logging == true)
      print_arr(winvals, winlen);
    else
      Serial.println(windex);

    windex %= winlen;

//    Serial.print(digitalRead(0));
//    Serial.print(digitalRead(1));
//    Serial.print(digitalRead(2));
//    Serial.print(digitalRead(3));
//    Serial.print("\t");
//    Serial.println(badpercent);
  }
} 
