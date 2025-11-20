# 🤖  Pia-the-μRSC [To Be]

## 📌Hardware Replication & Micro-RSC Development
<img src="Banner for Pia-the-uRSC.png" width="100%" style="max-height:200px; object-fit:cover;" />
I was inspired by [Pia-the-robot](https://github.com/BtreeComputingServcies/pia-the-robot), who was inspired by [Mira](https://www.youtube.com/watch?v=0vfuOW1tsX0) by Alonso Martinez.


## 🧠 Project Overview
This repository documents my full journey of replicating, assembling, and upgrading Pia-the-Robot, based on the original open-source design.

The main objectives are:
1. Rebuild Pia using [Raspberry Pi Pico](https://thepihut.com/products/raspberry-pi-pico-w?srsltid=AfmBOopVhjwxGJgmFiPiU_dQihIodUADGCJEcOd47JI0liRDAYfdv12_) and [DF9GMS 180° servos](https://www.dfrobot.com/product-1579.html?srsltid=AfmBOorRm1mJtgvEDg0HyJaaVKkh1eYbVWLtT9Ohvx80wH8pmlJqAed5)
2. Study expressive movement and mechanical design
3. Understand servo kinematics
4. Document full assembly, wiring, and coding steps
5. Adapt Pia into a cost-effective Micro-RSC platform for my BSc thesis

This project is continuously updated.

## 🔧 Hardware Used
| **Components** | Details |
|----------------|---------|
| **Microcontroller** | Raspberry Pi Pico |
| **Servos** | DF9GMS 180° micro servos (X, Y, Z axes) |
| **Magnets** | [6x3mm & 8x1mm](https://www.supermagnete.de/eng/disc-magnets-neodymium/disc-magnet-6mm-3mm_S-06-03-N?group=product_finder) (2 from each) |
| **3D Printed Parts** | All STL files from "Pia the Robot" on [Printables](https://www.printables.com/model/190775-pia-the-robot) |
| **Power** | USB 5V (initial) | 
| **Misc** | Jumper wires, screws, servo horns, breadboard |

## 🕹️ Servo Control Summary
Pia uses 3 servos controlled by PWM signals at 50 Hz.
1. Y-axis: head tilt to left and right
2. X-axis: head tolt to forward and backward
3. Z-axis: head rotation clockwise and anti-clockwise

Control uses a smooth-movement function that moves servos gradually by changing angle in small increments for natural motion.

## 🧩 3D Printed Parts
All parts were printed from the Pia-the-Robot model on [Printables.](https://www.printables.com/model/190775-pia-the-robot)

Status: All parts printed successfully.
