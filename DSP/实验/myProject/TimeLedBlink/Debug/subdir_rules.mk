################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
TimeLedBlink.obj: ../TimeLedBlink.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: "$<"'
	@echo 'Invoking: C2000 Compiler'
	"D:/file/3rd_down/DSP/ccs8/ccsv8/tools/compiler/ti-cgt-c2000_18.1.2.LTS/bin/cl2000" -v28 -ml -mt --include_path="D:/file/3rd_down/DSP/myProject/TimeLedBlink" --include_path="D:/file/3rd_down/DSP/ccs8/ccsv8/tools/compiler/ti-cgt-c2000_18.1.2.LTS/include" -g --diag_warning=225 --diag_wrap=off --display_error_number --preproc_with_compile --preproc_dependency="TimeLedBlink.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


