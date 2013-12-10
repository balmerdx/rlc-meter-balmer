################################################################################
# Automatically-generated file. Do not edit!
################################################################################


DEPS += \
	output/CMSIS/startup_stm32f30x.d \
	output/base/src/hw_config.d \
	output/base/src/main.d \
	output/base/src/stm32f30x_it.d \
	output/base/src/system_stm32f30x.d \
	output/base/src/usb_desc.d \
	output/base/src/usb_endp.d \
	output/base/src/usb_istr.d \
	output/base/src/usb_prop.d \
	output/base/src/usb_pwr.d \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_core.d \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_init.d \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_int.d \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_mem.d \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_regs.d \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_sil.d \
	output/StdPeriph_Driver/stm32f30x_adc.d \
	output/StdPeriph_Driver/stm32f30x_dac.d \
	output/StdPeriph_Driver/stm32f30x_dma.d \
	output/StdPeriph_Driver/stm32f30x_exti.d \
	output/StdPeriph_Driver/stm32f30x_gpio.d \
	output/StdPeriph_Driver/stm32f30x_misc.d \
	output/StdPeriph_Driver/stm32f30x_rcc.d \
	output/StdPeriph_Driver/stm32f30x_spi.d \
	output/StdPeriph_Driver/stm32f30x_syscfg.d \
	output/StdPeriph_Driver/stm32f30x_tim.d \


OBJS += \
	output/CMSIS/startup_stm32f30x.o \
	output/base/src/hw_config.o \
	output/base/src/main.o \
	output/base/src/stm32f30x_it.o \
	output/base/src/system_stm32f30x.o \
	output/base/src/usb_desc.o \
	output/base/src/usb_endp.o \
	output/base/src/usb_istr.o \
	output/base/src/usb_prop.o \
	output/base/src/usb_pwr.o \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_core.o \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_init.o \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_int.o \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_mem.o \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_regs.o \
	output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_sil.o \
	output/StdPeriph_Driver/stm32f30x_adc.o \
	output/StdPeriph_Driver/stm32f30x_dac.o \
	output/StdPeriph_Driver/stm32f30x_dma.o \
	output/StdPeriph_Driver/stm32f30x_exti.o \
	output/StdPeriph_Driver/stm32f30x_gpio.o \
	output/StdPeriph_Driver/stm32f30x_misc.o \
	output/StdPeriph_Driver/stm32f30x_rcc.o \
	output/StdPeriph_Driver/stm32f30x_spi.o \
	output/StdPeriph_Driver/stm32f30x_syscfg.o \
	output/StdPeriph_Driver/stm32f30x_tim.o \


output/CMSIS/startup_stm32f30x.o: Libraries/CMSIS/Device/ST/STM32F30x/Source/Templates/gcc_ride7/startup_stm32f30x.S
	@echo 'Building target: startup_stm32f30x.S'
	@$(CC) $(ASM_FLAGS) -o "$@" "$<"

output/base/src/hw_config.o: ./src/hw_config.c
	@echo 'Building target: hw_config.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/main.o: ./src/main.c
	@echo 'Building target: main.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/stm32f30x_it.o: ./src/stm32f30x_it.c
	@echo 'Building target: stm32f30x_it.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/system_stm32f30x.o: ./src/system_stm32f30x.c
	@echo 'Building target: system_stm32f30x.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/usb_desc.o: ./src/usb_desc.c
	@echo 'Building target: usb_desc.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/usb_endp.o: ./src/usb_endp.c
	@echo 'Building target: usb_endp.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/usb_istr.o: ./src/usb_istr.c
	@echo 'Building target: usb_istr.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/usb_prop.o: ./src/usb_prop.c
	@echo 'Building target: usb_prop.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/src/usb_pwr.o: ./src/usb_pwr.c
	@echo 'Building target: usb_pwr.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_core.o: ./Libraries/STM32_USB-FS-Device_Driver/src/usb_core.c
	@echo 'Building target: usb_core.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_init.o: ./Libraries/STM32_USB-FS-Device_Driver/src/usb_init.c
	@echo 'Building target: usb_init.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_int.o: ./Libraries/STM32_USB-FS-Device_Driver/src/usb_int.c
	@echo 'Building target: usb_int.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_mem.o: ./Libraries/STM32_USB-FS-Device_Driver/src/usb_mem.c
	@echo 'Building target: usb_mem.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_regs.o: ./Libraries/STM32_USB-FS-Device_Driver/src/usb_regs.c
	@echo 'Building target: usb_regs.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/base/Libraries/STM32_USB-FS-Device_Driver/src/usb_sil.o: ./Libraries/STM32_USB-FS-Device_Driver/src/usb_sil.c
	@echo 'Building target: usb_sil.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_adc.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_adc.c
	@echo 'Building target: stm32f30x_adc.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_dac.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_dac.c
	@echo 'Building target: stm32f30x_dac.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_dma.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_dma.c
	@echo 'Building target: stm32f30x_dma.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_exti.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_exti.c
	@echo 'Building target: stm32f30x_exti.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_gpio.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_gpio.c
	@echo 'Building target: stm32f30x_gpio.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_misc.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_misc.c
	@echo 'Building target: stm32f30x_misc.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_rcc.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_rcc.c
	@echo 'Building target: stm32f30x_rcc.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_spi.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_spi.c
	@echo 'Building target: stm32f30x_spi.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_syscfg.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_syscfg.c
	@echo 'Building target: stm32f30x_syscfg.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"

output/StdPeriph_Driver/stm32f30x_tim.o: Libraries/STM32F30x_StdPeriph_Driver/src/stm32f30x_tim.c
	@echo 'Building target: stm32f30x_tim.c'
	@$(CC) $(C_FLAGS) -o "$@" "$<"



