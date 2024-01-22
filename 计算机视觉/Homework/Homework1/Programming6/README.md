# 1. Environment Configuration

## 1.1 Installing dependencies

**opencv-4.7.0**

## 1.2 Steps  

First,create a `visual stdio ` project.

Second,we need properties configuration(**replace  the position of** **your own `opencv` folder)**.

1. Add follows to `Linker-General-Additional library directory`

    ```
    D:\Application\opencv\build\x64\vc16\lib
    ```

2. Add follows to`Linker-input-Additional Dependencies`

   ```
   opencv_world470d.lib
   ```

3. Add follows to `C/C++-General-Additional Include Directories`

    ```
    D:\Application\opencv\build\include
    ```

## 1.3 Preparing images 

Put your images `l,jpg` and `r.jpg` in the same directory with `main.cpp`.

# 2.Result

![](Programming6/Programming6/match.jpg)
