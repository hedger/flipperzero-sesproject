# Segger Embedded Studio project for Flipper Zero firmware

## Использование
### Зависимости

0. Добавить данный репозиторий в качестве сабмодуля в корень локальной копии репозитория `flipperzero-firmware`
1. Установить [Segger Embedded Studio for ARM](https://www.segger.com/downloads/embedded-studio)
2. Установить [gcc-arm-eabi-none](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) 
3. Скачать [OpenOCD](https://gnutoolchains.com/arm-eabi/openocd/) и добавить в PATH

### Настройка SES
5. Tools > Options > Building: 
	1. _Toolchain Root Directory_ установить в путь распакованного тулчейна + `/bin` (например, *`E:/tools/GNU Arm Embedded Toolchain/10 2021.10/bin`*)
	2. _Parallel Building Threads_ = число ядер процессора

6. Tools > Options > Environment > User Interface:

	1. _Application Main Font_ + _Application Monospace Font_ поправить на удобные значения
	2. _Theme_ = *`Dark`* / *`Operating System Default`*

7. Tools > Options > Languages:

	Для всех языков, установить _Indent Size_ и _Tab Size_ в 4


8. Tools > Options > Text Editor:

	1. Formatting > _Use .clang-format file_ = Yes (**ВАЖНО!** Позволяет форматировать код по кодстайлу нажанием ctrl+k ctrl+f)

	2. Formatting > _Formatting Indent Size_ = 4

	3. Visual Appearance > _Font_ = по вкусу

	4. Visual Appearance > _Line Numbers_ = *`All lines`*

## Настройки сборки 

SES использует концепцию "конфигураций" для формирования окончательных настроек солюшена. Конфигурации бывают публичные и приватные:
* Приватные содержат фрагмент настроек - опции компилятора, отладчика и т.д.;
* Публичные наследуют одну или несколько приватных конфигураций и собирают воедино настройки из них.

Также, в солюшене практически все его части - сам солюшен, отдельные проекты, отдельные папки и файлы в проекте - могут оверрайдить настройки под конкретную конфигурацию.

Данный солюшен поставляется с несколькими приватными конфигрурациями: 
* Конфиги под аппаратную ревизию Флиппера - F6 или F7
* Конфиги релизной и отладочной сборки
* Конфиги отладки через JLink и gdb/OpenOCD

...и двумя публичными, Release и Debug, в которых изначально выбран F7 и OpenOCD.

Изменить настройки можно в меню Projects > Build Configurations, изменив чекбоксы у публичных конфигураций.

## Отладка и прошивка из SES

* **Для сборки и загрузки прошивки в Флиппер под отладкой**: F5 (Debug > Go). 

* **Для подключения к Флипперу с уже работающей прошивкой**: Ctrl+T, D (Target > Disconnect)

* **Для отключения отладки**: Ctrl+T, H (Target > Attach Debugger)

**NB**: *В случае использования подключения через OpenOCD, при остановке отладки SES преждевременно убивает сервер gdb, из-за чего Флиппер остаётся приостановленным. Для обхода этой проблемы, можно запускать OpenOCD с помошью `start_gdb_openocd.cmd` - SES при запуске отладки подключится к нему, а не будет запускать свой инстанс сервера. При отключении отладки, этот инстанс OpenOCD не убивается SES, поэтому продолжение работы устройства корректно срабатывает. Подобной проблемы при подключении через JLink нет.* 

TODO: отдельные скрипты обновления прошивки через OpenOCD.

## Прочее
Солюшен автоматически загружает все необходимые файлы с кодом при загрузке. Однако, если добавить файл в проект во время работы IDE, необходимо синхронизировать дерево файлов: Project > Reload Flipper.