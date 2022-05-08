# Segger Embedded Studio project for Flipper Zero firmware

## Установка

0. Добавить данный репозиторий в качестве сабмодуля в корень локальной копии репозитория `flipperzero-firmware`
```
git submodule add https://github.com/hedger/flipperzero-sesproject.git sesproject
git submodule update --init --recursive
```

### Зависимости

1. Установить [Segger Embedded Studio for ARM](https://www.segger.com/downloads/embedded-studio)
2. Установить [gcc-arm-eabi-none](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) 
3. Скачать [OpenOCD](https://gnutoolchains.com/arm-eabi/openocd/) и добавить в PATH
4. Python 2+ для скрипта автоматического обновления версии сборки

### Начальная конфигурация SES
5. Tools > Options > Building: 
	1. В _Global Macros_ добавить `GCCRoot` со значением пути распакованного тулчейна + `/bin` (например, *`GCCRoot=D:/Tools/GNU Arm Embedded Toolchain/10 2021.10/bin`*)
	2. _Parallel Building Threads_ = число ядер процессора

6. Tools > Options > Environment > User Interface:

	1. _Application Main Font_ + _Application Monospace Font_ поправить на удобные значения
	2. _Theme_ = *`Dark`* / *`Operating System Default`*

7. Tools > Options > Languages:

	Для всех языков установить _Indent Size_ и _Tab Size_ в 4


8. Tools > Options > Text Editor:

	1. Formatting > _Use .clang-format file_ = Yes (**ВАЖНО!** Позволяет форматировать код по кодстайлу нажанием ctrl+k ctrl+f)

	2. Formatting > _Formatting Indent Size_ = 4

	3. Visual Appearance > _Font_ = по вкусу

	4. Visual Appearance > _Line Numbers_ = *`All lines`*

## Настройки сборки 

SES использует концепцию "конфигураций" для формирования окончательных настроек солюшена. Конфигурации бывают публичные и приватные:
* Приватные содержат фрагмент настроек - опции компилятора, отладчика и т.д.;
* Публичные наследуют одну или несколько приватных конфигураций и собирают воедино настройки из них.

Также в солюшене практически все его части - сам солюшен, отдельные проекты, отдельные папки и файлы в проекте - могут оверрайдить настройки под конкретную конфигурацию, публичную или приватную.

Данный солюшен поставляется с несколькими приватными конфигрурациями: 
* Конфиги под аппаратную ревизию Флиппера - F6 или F7
* Конфиги релизной и отладочной сборки
* Конфиги отладки через JLink и gdb/OpenOCD

...и двумя публичными, Release и Debug, в которых изначально выбран F7 и OpenOCD.

Настроить публичные конфигурации можно в меню Projects > Build Configurations, изменив чекбоксы у приватных конфигураций.

### Поддержка [CCache](https://github.com/ccache/ccache)

Проект поддерживает ускорение повторных сборок с использованием CCache. 
Под Windows, достаточно скачать собранный ccache.exe и разместить либо в PATH, либо в папке `/bin` тулчейна.

По умолчанию поддержка CCache отключена, её можно добавить во все конфигурации через меню настройки сборки (Alt+Return при выбранном с дереве солюшене).

## Отладка и прошивка из SES

* **Для сборки и загрузки прошивки в Флиппер под отладкой**: F5 (Debug > Go). 

* **Для подключения к Флипперу с уже работающей прошивкой**: Ctrl+T, H (Target > Attach Debugger)

* **Для отключения отладки**: Ctrl+T, D (Target > Disconnect)

**NB**: *В случае использования подключения через OpenOCD, при остановке отладки SES преждевременно убивает сервер gdb, из-за чего Флиппер остаётся приостановленным. Для обхода этой проблемы можно запускать OpenOCD с помошью `scripts/start_gdb_openocd.cmd` - SES при запуске отладки подключится к нему, а не будет запускать свой инстанс сервера. При отключении отладки этот инстанс OpenOCD не убивается SES, поэтому продолжение работы устройства корректно срабатывает. Подобной проблемы при подключении через JLink нет.* 

### Скрипты

Для прошивки firmware и bootloader без использования SES подготовлены скрипты в папке `scripts`. Для записи используется сборка под таргет f7. Запись выполняется через OpenOCD, необходимо его наличие в `PATH`.

## Прочее
* Солюшен автоматически загружает все необходимые файлы с кодом при загрузке. Однако, если создать файл в файловой системе во время работы IDE, необходимо синхронизировать дерево солюшена: Project > Reload Flipper.

* Файл проекта `flipperzero.emSession` - простой XML, многие опции проще править руками прямо в нём, чем разбираться с выбором конфигурации в интерфейсе SES.

* Дефайны для `firmware` с флагами и выбором приложений редактируются либо прямо в файле проекта, либо через SES:
	- выбрать проект в дереве солюшена, открыть свойства;
	- выбрать конфигурацию "Common";
	- отредактировать Code > Preprocessor > Preprocessor Definitions.
