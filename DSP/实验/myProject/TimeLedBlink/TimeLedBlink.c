// TI File $Revision: /main/3 $
// Checkin $Date: December 17, 2009   14:38:27 $
//###########################################################################
//
// FILE:    Example_2802xLedBlink.c
//
// TITLE:   DSP2802x LED Blink Getting Started Program.
//
// ASSUMPTIONS:
//
//    This program requires the DSP2802x header files.
//
//
//    As supplied, this project is configured for "boot to SARAM"
//    operation.  The 2802x Boot Mode table is shown below.
//
//    $Boot_Table
//    While an emulator is connected to your device, the TRSTn pin = 1,
//    which sets the device into EMU_BOOT boot mode. In this mode, the
//    peripheral boot modes are as follows:
//
//      Boot Mode:   EMU_KEY        EMU_BMODE
//                   (0xD00)	     (0xD01)
//      ---------------------------------------
//      Wait		 !=0x55AA        X
//      I/O		     0x55AA	         0x0000
//      SCI		     0x55AA	         0x0001
//      Wait 	     0x55AA	         0x0002
//      Get_Mode	 0x55AA	         0x0003
//      SPI		     0x55AA	         0x0004
//      I2C		     0x55AA	         0x0005
//      OTP		     0x55AA	         0x0006
//      Wait		 0x55AA	         0x0007
//      Wait		 0x55AA	         0x0008
//      SARAM		 0x55AA	         0x000A	  <-- "Boot to SARAM"
//      Flash		 0x55AA	         0x000B
//	    Wait		 0x55AA          Other
//
//   Write EMU_KEY to 0xD00 and EMU_BMODE to 0xD01 via the debugger
//   according to the Boot Mode Table above. Build/Load project,
//   Reset the device, and Run example
//
//   $End_Boot_Table
//
// DESCRIPTION:
//
//    This example configures CPU Timer0 for a 500 msec period, and toggles the GPIO34
//    LED  once per interrupt. For testing purposes, this example
//    also increments a counter each time the timer asserts an interrupt.
//
//       Watch Variables:
//          CpuTimer0.InterruptCount
//
//       Monitor the GPIO34 LED blink on (for 500 msec) and off (for 500 msec) on the 2802x control card.
//
//###########################################################################
// $TI Release: 2802x C/C++ Header Files V1.25 $
// $Release Date: December 18, 2009 $
//###########################################################################


#include "DSP28x_Project.h"     // Device Headerfile and Examples Include File

// Prototype statements for functions found within this file.
interrupt void cpu_timer0_isr(void);

void main(void)
{

// Step 1. Initialize System Control:
// PLL, WatchDog, enable Peripheral Clocks
// This example function is found in the DSP2802x_SysCtrl.c file.
   InitSysCtrl();

// Step 2. Initalize GPIO:
// This example function is found in the DSP2802x_Gpio.c file and
// illustrates how to set the GPIO to it's default state.
// InitGpio();  // Skipped for this example


// Step 3. Clear all interrupts and initialize PIE vector table:
// Disable CPU interrupts
   DINT;

// Initialize the PIE control registers to their default state.
// The default state is all PIE interrupts disabled and flags
// are cleared.
// This function is found in the DSP2802x_PieCtrl.c file.
   InitPieCtrl();

// Disable CPU interrupts and clear all CPU interrupt flags:
   IER = 0x0000;
   IFR = 0x0000;

// Initialize the PIE vector table with pointers to the shell Interrupt
// Service Routines (ISR).
// This will populate the entire table, even if the interrupt
// is not used in this example.  This is useful for debug purposes.
// The shell ISR routines are found in DSP2802x_DefaultIsr.c.
// This function is found in DSP2802x_PieVect.c.
   InitPieVectTable();

// Interrupts that are used in this example are re-mapped to
// ISR functions found within this file.
   EALLOW;  // This is needed to write to EALLOW protected registers
   PieVectTable.TINT0 = &cpu_timer0_isr;
   EDIS;    // This is needed to disable write to EALLOW protected registers

// Step 4. Initialize the Device Peripheral. This function can be
//         found in DSP2802x_CpuTimers.c
   InitCpuTimers();   // For this example, only initialize the Cpu Timers
// Configure CPU-Timer 0 to interrupt every 500 milliseconds:
// 60MHz CPU Freq, 50 millisecond Period (in uSeconds)
   ConfigCpuTimer(&CpuTimer0, 60, 500000);


// To ensure precise timing, use write-only instructions to write to the entire register. Therefore, if any
// of the configuration bits are changed in ConfigCpuTimer and InitCpuTimers (in DSP2802x_CpuTimers.h), the
// below settings must also be updated.

   CpuTimer0Regs.TCR.all = 0x4001; // Use write-only instruction to set TSS bit = 0

// Step 5. User specific code, enable interrupts:

// Configure GPIO34 as a GPIO output pin
   EALLOW;
   GpioCtrlRegs.GPBMUX1.bit.GPIO34 = 0;
   GpioCtrlRegs.GPBDIR.bit.GPIO34 = 1;
   EDIS;

// Enable CPU INT1 which is connected to CPU-Timer 0:
   IER |= M_INT1;

// Enable TINT0 in the PIE: Group 1 interrupt 7
   PieCtrlRegs.PIEIER1.bit.INTx7 = 1;

// Enable global Interrupts and higher priority real-time debug events:
   EINT;   // Enable Global interrupt INTM
   ERTM;   // Enable Global realtime interrupt DBGM

// Step 6. IDLE loop. Just sit and loop forever (optional):
   for(;;);
}


interrupt void cpu_timer0_isr(void)
{
   CpuTimer0.InterruptCount++;
   GpioDataRegs.GPBTOGGLE.bit.GPIO34 = 1; // Toggle GPIO34 once per 500 milliseconds
   // Acknowledge this interrupt to receive more interrupts from group 1
   PieCtrlRegs.PIEACK.all = PIEACK_GROUP1;
}


//===========================================================================
// No more.
//===========================================================================
