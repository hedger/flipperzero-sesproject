@echo off
SET OPENOCD_BASE_ARGS=-f interface/stlink.cfg -c "transport select hla_swd" -f "../xtras/stm32wbx.cfg" -c "stm32wbx.cpu configure -rtos auto" -c "init"

SET FLASH_BIN=%1
SET FLASH_ADDR=%2
SET TARGET=f7

rem if /i "%3" neq "" set TARGET=%3

echo Writing %FLASH_BIN% @ %FLASH_ADDR%

REM optionally add 'verify' to program args
openocd %OPENOCD_BASE_ARGS% -c "program %FLASH_BIN% reset exit %FLASH_ADDR%"