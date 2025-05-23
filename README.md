PAV - P5: síntesis musical polifónica
=====================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 5](https://github.com/albino-pav/P5) 
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde que
los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A modo de memoria de la práctica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.


*mencionar que todos nuestros comentarios son escritos en cursivo*

### Envolvente ADSR.

Tomando como modelo un instrumento sencillo (puede usar el InstrumentDumb), genere cuatro instrumentos que permitan visualizar el funcionamiento de la curva ADSR.

* Un instrumento con una envolvente ADSR genérica, para el que se aprecie con claridad cada uno de sus parámetros: ataque (A), caída (D), mantenimiento (S) y liberación (R).

  - *Podemos observar una ADSR genérica, con un ataque del 10% de duración, una caída del 20%, un mantenimiento del 50% y una liberación final del 20% (porcentajes relativos a un intervalo de tiempo determinado).* 

  ![gráfica de una ADSR genérica](img/ADSR_generica.png)
  
  - *A continuación, se muestra un ejemplo específico utilizando el instrumento `seno` (con los parámetros de la envolvente ADSR anteriores) para la generación de la primera nota "do" del archivo `doremi.sco`. El archivo de audio resultante se llama `seno.wav`. El comando utilizado para generar el archivo de audio es:*

    ```sh
    synth seno.orc doremi.sco seno.wav
    ```

    *La gráfica a continuación ilustra las fases de Ataque (A), Decaimiento (D), Mantenimiento (S) y Liberación (R) de la señal de audio generada:*

    ![ADSR Curve](img/ADSR_doremi_seno.png)

    *En esta gráfica, podemos observar claramente cómo la envolvente ADSR se aplica a una nota específica del instrumento `seno`.*

* Un instrumento *percusivo*, como una guitarra o un piano, en el que el sonido tenga un ataque rápido, no haya mantenimiemto y el sonido se apague lentamente.

  - Para un instrumento de este tipo, tenemos dos situaciones posibles:

    * El intérprete mantiene la nota *pulsada* hasta su completa extinción.

      - *podemos observar como no hay existencia (almenos apreciable) de la región de mantenimiento, y la caída hacia 0 del instrumento se compone de una decaída progresiva y gradual.*

      ![gráfica de una ADSR percusiva (1)](img/ADSR_percusivo1.png)

      *La generación de la forma de onda con dichos parámetros propios de un instrumento percusivo con dichas características se volvió a realizar con el programa `synth`, de las misma forma que se hizo con el primer instrumento. Se volvió a usar la primera nota **do** de la orquestación `DoReMi`.*

      ![ADSR Curve](img/ADSR_doremi_percussive1.png)

    * El intérprete da por finalizada la nota antes de su completa extinción, iniciándose una disminución abrupta del sonido hasta su finalización.

      - *Ahora el tramo de liberación debe suponer una mayor extensión, debido a que, como dice el enunciado, el intérprete ha dado por finalizada la nota "antes de tiempo".*

      ![gráfica de una ADSR percusiva (2)](img/ADSR_percusivo2.png)

      *La representación de la forma de onda para este tipo de ADSR se visualiza imediatamente abajo, donde la decaída del instrumento debido a la finalización por el intérprete se representa con una pérdida de envolvente de carácter exponencial:*

      ![ADSR Curve](img/ADSR_doremi_percussive2.png)

  - Debera representar en esta memoria **ambos** posibles finales de la nota.

* Un instrumento *plano*, como los de cuerdas frotadas (violines y semejantes) o algunos de viento. En ellos, el ataque es relativamente rápido hasta alcanzar el nivel de mantenimiento (sin sobrecarga), y la liberación también es bastante rápida.

  - *podemos ver como el ADSR descrito abajo cumple con las condiciones de dicho tipo de instrumento:*

  ![gráfica de una ADSR plana](img/ADSR_plano.png)

  *Y como siempre, la ejecución de la orquestación `DoReMi` mediante el programa `synth` con un instrumento seno del tipo "plano" puede verse a continuación (como siempre, solo se representa la primer nota de la orquestación, el `do`).*

  ![ADSR Curve](img/ADSR_doremi_plano.png)

Para los cuatro casos, deberá incluir una gráfica en la que se visualice claramente la curva ADSR. Deberá añadir la información necesaria para su correcta interpretación, aunque esa información puede reducirse a colocar etiquetas y títulos adecuados en la propia gráfica (se valorará positivamente esta alternativa).

---
---

### Instrumentos Dumb y Seno.

Implemente el instrumento `Seno` tomando como modelo el `InstrumentDumb`. La señal **deberá** formarse mediante búsqueda de los valores en una tabla.

- Incluya, a continuación, el código del fichero `seno.cpp` con los métodos de la clase Seno.

```cpp
#include <iostream>
#include <math.h>
#include "seno.h"
#include "keyvalue.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

InstrumentSeno::InstrumentSeno(const std::string &param)
    : adsr(SamplingRate, param)
{
  bActive = false;
  x.resize(BSIZE);

  /*
    You can use the class keyvalue to parse "param" and configure your instrument.
    Take a Look at keyvalue.h
  */
  KeyValue kv(param);
  int N;
  if (!kv.to_int("N", N))
    N = 40; // default value

  /*additionally, we can add another parameter that dictates the mode of tbl values extractions where:

    - 0 == no interpolation
    - 1 == interpolation (first_value + second_value)/2
  */

  if (kv("I") != "false")
    Interpolation = false; // default value
  else
  {
    Interpolation = true;
  }

  /*we can also implemented seno instrument to be percussive (with exponential final decay)*/
  if (kv("percussive") == "true")
    percussive = true; // default value
  else
  {
    percussive = false;
  }

  // Create a tbl with one period of a sinusoidal wave
  tbl.resize(N);
  float phase = 0, step = 2 * M_PI / (float)N;
  index = 0;
  for (int i = 0; i < N; ++i)
  {
    tbl[i] = sin(phase);
    phase += step;
  }
}

void InstrumentSeno::command(long cmd, long note, long vel)
{
  f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f); // convertion of NOTE to FREQ

  if (cmd == 9)
  { //'Key' pressed: attack begins
    bActive = true;
    adsr.start();
    index = 0;
    phas = 0.0f;
    increment = ((f0 / SamplingRate) * tbl.size());
    A = vel / 127.;
    // A = std::clamp(static_cast<float>(vel) / 127.0f, 0.0f, 1.0f);
  }
  else if (cmd == 8)
  { //'Key' released: sustain ends, release begins
    adsr.stop();
    end_hit = true;
  }
  else if (cmd == 0)
  { // Sound extinguished without waiting for release to end
    adsr.end();
  }
}

const vector<float> &InstrumentSeno::synthesize()
{
  if (not adsr.active())
  {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  /*En general, al recorrer la tabla con los saltos adecuados para producir una cierta
  frecuencia fundamental, será necesario acceder a índices no enteros de la tabla. Es
  decir, el valor deseado no se corresponde con ninguno de los que están almacenados
  en ella, sino a uno intermedio entre dos que sí lo están (que pueden ser el último y el
  primero...).

  ◦ En primera aproximación, puede redondear el índice requerido a entero y usar
  para la muestra uno de los valores almacenados en la tabla. <-- LO QUE ESTAMOS USANDO AHORA

  ⋄ Pero esta solución introduce una distorsión que es claramente audible.

  ◦ Como trabajo de ampliación, se propone calcular el valor de la muestra como
  interpolación lineal entre los valores inmediatamente anterior y posterior al índice
  deseado (pero recuerde que el siguiente del último es el primero...)*/
  for (unsigned int i = 0; i < x.size(); ++i)
  {
    phas += increment;
    /*if percussive == true and note end has been hit*/
    if (percussive && end_hit)
    {
      if (std::floor(phas) == phas || !Interpolation)
      {
        x[i] = A * tbl[round(phas)] * pow(0.99935, (int)interrupted_index);
        interrupted_index++;
      }
      else // phas is a non intger, we must interpolate
      {
        x[i] = A * getInterpolatedValue(phas) * pow(0.99935, (int)interrupted_index);
        interrupted_index++;
      }
    }
    else
    {
      if (std::floor(phas) == phas || !Interpolation)
      {
        x[i] = A * tbl[round(phas)];
      }
      else // phas is a non intger, we must interpolate
      {
        x[i] = A * getInterpolatedValue(phas);
      }
    }
    while (phas >= tbl.size())
      phas = phas - tbl.size();
  }
  adsr(x); // apply envelope to x and update internal status of ADSR

  return x;
}

/*en caso de quer realizar la ampliación como dice arriba, podemos realizar la interpolación
   de la siguiente manera:*/

float InstrumentSeno::getInterpolatedValue(const float phas)
{

  int tbl_size = tbl.size();
  // static_cast/size_t types for multi-platform compatibility
  size_t lowerIndex = static_cast<size_t>(std::floor(phas));
  size_t upperIndex = static_cast<size_t>(std::ceil(phas));

  // Boundary conditions for lowerIndex and upperIndex
  if (lowerIndex >= tbl_size || upperIndex >= tbl_size)
  {
    lowerIndex = tbl_size - 1;
    upperIndex = 0;
  }

  // Interpolate between tbl[lowerIndex] and tbl[upperIndex]
  float lowerValue = tbl[lowerIndex];
  float upperValue = tbl[upperIndex];

  return (lowerValue + upperValue) / 2;
}

```
- Explique qué método se ha seguido para asignar un valor a la señal a partir de los contenidos en la tabla, e incluya una gráfica en la que se vean claramente (use pelotitas en lugar de líneas) los valores de la tabla y los de la señal generada.

  *Como se ve en el `for()` del constructor de la clase **InstrumentSeno**, la tabla se construye en base a un periodo entero de una señal senoidal como cualquier otra, en incrementos que van en función del número de muestras que deseamos tener dentro de la tabla, es decir, como más puntos almacenemos, más pequeños serán los incrementos y por lo tanto tendremos el equivalente de un periodo de senoide almacenado en la tabla muestreado con frecuencia de muestreo más alta.*

  *Cuando los valores estén ya dentro de la tabla, la recorremos con una velocidad determinada, cosa que viene dada por la frecuencia fundamental del propio instrumento seno mediante la conversión de **note** (valor determinado por el fichero `.sco`) a f0:*

  ```cpp
  f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f);
  ```

  *El recorrido de la tabla se realiza posterior a una llamada al método **command()**, donde en caso de iniciarse una nota, declaramos la variable que nos indica la velocidad a la cual recorrer la tabla, cuya línia de código se explicita a continuación:*

  ```cpp
  increment = ((f0 / SamplingRate) * tbl.size());
  ```

  *Gracias a esta variable, cuando llamemos al método **synthesize()**, podremos recorrer la tabla a la velocidad deseada. Por ejemplo, si nuestra tabla almacena 40 valores (valor default de N (tamaño de `tbl`)) para recorrer la tabla a velocidad de muestra a muestra (sin saltarnos ninguna, que en teoría podría entenderse como la velocidad más baja, aunque también sería posible ir 1/2 o 1/4 o menos de muestras/tick) nuestra frecuencia fundamental `f0` debe ser un 1/40 de la frecuencia de muestreo (declarada como `SamplingRate` en el código) que equivale a 44100 Hz.*

  *En este caso, el señal base reproducido por el instrumento Seno sería idéntico al señal almacenado en `tbl[n]`. A continuación graficamos en rojo el señal `tbl[n]` junto con la reproducción del instrumento Seno cuando se cumplen dichas condiciones de `f0`. Se ha sumado 1 al señal `x[n]` para que pudiera distinguirse del señal base `tbl[n]`:*

  ![visualización señal base tbl[n] con x[n] cuando f0 = Fs/40](img/SR:40_noInterpolation.png)

  *De hecho esta perfecta alineación entre los señales se producirá siempre que `f0` sea la N-ésima parte de la frecuencia de muestreo `SamplingRate`, donde N es el tamaño de la tabla.*

  *Si quisiéramos recorrer la tabla a mayor velocidad y por lo tanto saltarnos muestras, como por ejemplo, ir de 2 en 2 muestras (el doble del caso anterior), debemos fijar `f0` al doble, por lo tanto a un 1/20 del `SamplingRate`. En este caso, el señal obtenido en base a la tabla `tbl` se construiria de la siguiente forma (si x[n] es el señal del instrumento y tbl[n] es la tabla donde se contienen los valores por defecto):*

  *x[0] = tbl[1], x[1] = tbl[3], x[2] = tbl[5] ...*

  *A continuación mostramos un gráfico donde se puede visualizar de forma semejante al anterior gráfica, la diferencia entre las 2 señales, donde a `x[n]` se le ha sumado 1 para que pueda diferenciarse mejor de la otra señal. Hemos de tener en cuenta que aunque parezca que ambas señales estén durando lo mismo, cuando se vaya a realizar la orquestración, la reproducción de un instrumento se realiza a base de ticks/segundo y como `x[n]` ahora tiene menos puntos por periodo que la `x[n]` del apartado anterior (la mitad exactamente), ésta se reproduciría el doble de rápido y así es como aconseguiríamos la percepción de una `f0` distinta:*

  ![gráfico de muestras de la tabla vs señal construido](img/SR:20_noInterpolation.png)

*Hasta ahora la recogida de valores desde `tbl[n]` se ha heco de forma exacta, es decir, no hay ambiguedad sobre que valores de la tabla escoger, ya que los incrementos eran enteros (en el primer caso de f0 = SamplingRate/40, el incremento era de 1 en 1 mientras que en el segundo caso el incremento era el doble, 2). También nos gustaría enseñar lo que sucedería cuando dichos incrementos no son tan perfectos, y nos encontramos en la situación de tener que coger valores de la tabla intermedios, por ejemplo, si incremento = 1.5, los valores a los que accederíamos en `tbl[n]` serian `tbl[0], tbl[1.5], tbl[3], tbl[4.5]...`. Se han implementado 2 soluciones para redimiarlo:*

* *Aproximación del índice decimal al entero más próximo e.g. 4.5 -> 5 o 3.4 = 3. Llamámosle el caso **1**.*

* *Interpolación Ponderada (Weighed Interpolation) e.g. si el índice = 4.7, interpolamos entre las muestras del índice 4 y 5 pero tal que 70% de la contribución proviene del índice 5 y el 30% de la contribución proviene de índice 4. Llamámosle el caso **2**.*

*En cuanto el **caso 1**, este procedimiento se realiza con la ejecución de:*

```cpp
x[i] = A * tbl[round(phas)];
```
*Este método de resolución de índices puede ser problemática cuando se desee reproducir un señal con alta fidelidad y reducir las distorsiones incorporadas por dicha aproximación. Ocurrirá distorsión siempre que la `f0` que se esté emulando no sea un múltiplo exacto de 44100/N donde N es el tamaño de `tbl[n]`. En nuestro caso, N=40 y por lo tanto cualquier nota músical cuya equivalente `f0` no sea un múltiplo entero de 1102,5 Hz tendrá distorsión. Veamos un ejemplo donde usamos 2 notas músicales relativamente próximas en cuanto a la `f0` y observemos como realmente hay presencia de distorsión.*

*Vamos a visualizar las "diferentes" formas de onda producidas por el instrumento Seno cuando queremos emular la nota `69` (`f0 = 440 Hz`) y luego la nota `73` (`f0 = 554 Hz`):*

*Antes dijimos que para que el Seno cogiese todos los valores de la tabla (N=40), la `f0` de su nota tenia que ser 44100/40 = 1102.5 Hz. La nota 69 tiene un `f0` de 440 Hz, por lo tanto deberemos recorrer `tbl[n]` a mucha menor velocidad y tendremos que "inventarnos" valores en medio de otros dentro de la tabla. Aproximadamente, tendremos que "inventarnos" unos 2-3 muestras entre índices de la tabla sucesivos (1/40 / 440/44100). Si graficamos junto este señal otro con una `f0` parecida pero algo distinta, como por ejemplo la nota 73 cuyo `f0` equivale a unos 554 Hz, recorreremos la tabla un poco más rápida pero, lo importante de entender de este análisis, es el hecho que este método de aproximación del índice supone distorsión aparente ya que muestras sucesivas deben repetirse entre sí (básicamente cuando se usan frecuencias por debajo de los comentados 1102,5 Hz). Esto no es un efecto que se produce cuando se usan frecuencias fundamentales superiores a dicho valor, aunque siempre que no implementemos un método de interpolación inteligente, siempre estaremos limitados a los valores proporcionados por la tabla inicial. Más de esto después de la gráfica:*

![gráfica de tbl[n] vs 2 señales de 2 notas distintas, sin interpolación](img/Note69vs73.png)
*Notar que x[n] es la senoide de la nota 69 mientras que y[n] es de la nota 73.*

*En cuanto al **caso 2**, su implementación se realizó para evitar los sucesos que suceden con el caso 1, donde hay muestras sucesivas repetidas, por falta de dicha interpolación. Vamos a enseñar una figura donde hay 2 gráifcas emparejadas, la de arriba representando el máximo de una forma de onda de un instrumento tipo seno con interpolación activado y la de abajo representando el mismo instrumento pero con interpolación desactivada:*

![Gráficas Seno Con Interpolación vs Sin Interpolación](img/seno_vibrato_normal_conInterpolacion.png)

*No es difícil de argumentar a favor del método con interpolación activado, el cual es claramente superior en todos los casos, por lo tanto se aconseja que para cualquier síntesis de instrumento se aplique dicho instrumento con interpolación activada. Nosotros nos hemos asegurado de aplicar interpolación a cada uno de nuestros instrumentos por defecto, ya que es el método claramente superior.*


- Si ha implementado la síntesis por tabla almacenada en fichero externo, incluya a continuación el código
  del método `command()`.

```cpp
void InstrumentSeno::command(long cmd, long note, long vel) {
    f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f); // Conversión de nota a frecuencia

    if (cmd == 9) { // 'Key' pressed: attack begins
        bActive = true;
        adsr.start();
        index = 0;
        phas = 0.0f;
        increment = ((f0 / SamplingRate) * tbl.size());
        A = vel / 127.0f;
        
        // Cargar la tabla desde un fichero externo
        std::ifstream file("sine_table.dat");
        if (file.is_open()) {
            for (int i = 0; i < tbl.size(); ++i) {
                file >> tbl[i];
            }
            file.close();
        } else {
            std::cerr << "Error: no se pudo abrir el archivo sine_table.dat" << std::endl;
        }
    } else if (cmd == 8) { // 'Key' released: sustain ends, release begins
        adsr.stop();
    } else if (cmd == 0) { // Sound extinguished without waiting for release to end
        adsr.end();
    }
}
```  

---
---

# Efectos sonoros.

- Incluya dos gráficas en las que se vean, claramente, el efecto del trémolo y el vibrato sobre una señal sinusoidal. Deberá explicar detalladamente cómo se manifiestan los parámetros del efecto (frecuencia e índice de modulación) en la señal generada (se valorará que la explicación esté contenida en las propias gráficas, sin necesidad de *literatura*).

## *Trémolo*

*Para la demostración del efecto del trémolo vamos a hacer una comparativa entre la aplicación de dicho efecto con unos parámetros más "normales" o cómodos (A=0.15 y fm=10Hz) y otra con parámetros más "agresivos" (A=1.5 y fm=10Hz). A continuacíon enseñamos el proceso de obtención de una nota bajo el efecto del trémolo y su clara apariencia en la representación gráifca del señal. Empezemos por el trémolo con parámetros "normales":*

## *Tremolo Normal*

*Primero se partió de los siguientes ficheros para generar el `.wav` de donde extraeríamos la señal a analizar:*

***doremi.sco***

```shell
#Time; On (8)/Off (9); Channel; Note; Velocity;
#Time; Control; Channel; Effect; On/Off;
0	9	1	60	100
120	8	1	60	100
0   12  1   13  1 #trémolo inicio
40	9	1	62	100
120	8	1	62	100
40	9	1	64	100
120	8	1	64	100
40	9	1	65	100
120	8	1	65	100
40	9	1	67	100
120	8	1	67	100
40	9	1	69	100
120	8	1	69	100
40	9	1	71	100
0   12  1   13  0 #trémolo final
120	8	1	71	100
40	9	1	72	100
120	8	1	72	100
40	0	1	0	0
```

***effects.orc***

```shell
13	Tremolo	fm=10; A=0.15;
```

***seno.orc***

```shell
1	InstrumentSeno	ADSR_A=0.02; ADSR_D=0.1; ADSR_S=0.4; ADSR_R=0.1; N=40; I=false; percussive=false; 
```

*Luego ejecutamos el programa `synth` de la siguiente manera (ubicandonos dentro de `work/`) que dió lugar al fichero de sonido `seno_tremolo_norma.wav` (todos los ficheros de sonidos realizados a lo largo de la práctica estan presentes en el mismo directorio de `work/` por si al lector le apetece):*

```shell
synth -e effects.orc seno.orc doremi.sco seno_tremolo_normal.wav
```

*A partir de este fichero de audio, podemos extraer la siguientes gráficas del señal contenido en él:*

*Gráfica del do-re-mi con el efecto trémolo (normal) aplicado sobre él:*

![Gráfica del do-re-mi con el efecto trémolo (normal)](img/seno_tremolo_normal_noInterpolation.png)

*Imagen generada a partir del código Python en `scripts/tremolo.py`*

*Gráfica de la nota Re ampliada destacando zona de aplicación de un período de Trémolo:*

![Gráfica de la nota Re ampliada](img/seno_tremolo_normal_noInterpolation_zoom.png)

*Imagen generada a partir del código Python en `scripts/tremolo3.py`*

*El fichero de audio de salida (`.wav`) del do-re-mi con éste trémolo de baja potencia aplicado se halla, como todos los ficheros de audio, en el directorio `work/` y se llama **seno_tremolo_normala.wav**.*

## *Tremolo Agresivo*

*Ahora pasamos a aplicar un efecto del tremolo aún más fuerte. Para cambiar las propidades del efecto, basta con modificar el fichero `work/effects.orc`, que ahora cogerá la siguiente forma:*

```shell
13  Tremolo	fm=10; A=1.5;
```

*Es decir, aumentamos la amplitud de modulación a un 150%, cosa que debería reflejarse como una variación mucha más brusca de la amplitud de las notas de la orquestración. Vamos a verlo ejecutando el comando `synth` enseñado anteriormente con exactamente la misma estructura, solo que ahora cambiamos el fichero de audio de salida por uno llamado `seno_tremolo_agresivo.wav`.*

```shell
synth -e effects.orc seno.orc doremi.sco seno_tremolo_agresivo.wav
```

*Procedemos a analizar el señal con cada vez más detalle. Aquí tenemos la gráfica de la orquestación do-re-mi con efecto tremolo "agresivo" aplicado:*

![DoReMi con Tremolo Agresivo](img/seno_tremolo_agresivo_noInterpolation.png)

*Miramos que está ocurriendo en esas notas intermedias de la orquestación (donde el efecto se está aplicando):*

![Nota Re Bajo Efecto Del Tremolo Agresivo](img/seno_tremolo_agresivo_noInterpolation_oneNote.png)


*Si miramos aún un poco más cerca, igual como hicimos con el efecto anterior del tremolo "normal":*

![Ampliación Nota Re Bajo Efecto Del Tremolo Agresivo](img/seno_tremolo_agresivo_noInterpolation_zoom.png)

*Imagen generada a partir del código Python en `scripts/tremolo3.py`*


*Podemos apreciar como el tremolo, aplicado con parámetros más "extravagantes", realmente da lugar a transformaciones del señal interesantes y que pueden ser útiles a la hora de sintetizar sonidos únicos. También destacar la información de alta calidad que nos proporciona la leyenda de esta imagen. Si tenemos en cuenta que el tremolo aplicado ha sido uno con frecuencia de modulación 10 Hz, tiene sentido que un periodo de modulación de la amplitud dure 100 ms (una décima de un segundo) como se ha podido comprobar también de forma empírica, donde el primer máximo se encuenra al instante 0,89 segundos y el siguiente más próximo a 0,99 segundos.*

---
---

## *Vibrato*

*El efecto Vibrato consiste en una modulación periódica de la frecuencia de la señal de audio. Esta modulación produce una variación en el tono que puede ser percibida como un ligero temblor o vibración en el sonido. En el contexto de los efectos de audio, el Vibrato puede ajustarse para ser sutil o muy pronunciado, según los parámetros utilizados.*

*Para analizar el efecto Vibrato, hemos creado dos configuraciones: un Vibrato "leve" o "normal" con una ligera modulación (I=0.5 y fm=10Hz) y un Vibrato "fuerte" o "agresivo" con una modulación más pronunciada (I=24 y fm=200Hz). A continuación, se describen ambos casos y su impacto en la señal de audio, tanto en el dominio temporal como frecuencial.*

### *Vibrato Normal*

*Para la generación de una orquesta con efecto de vibrato normal (I=0.5 y fm=10Hz) hemos modificado los siguientes ficheros:*

***effects.orc***

*Hemos añadido la siguiente línea de metadatos:*

```shell
14  Vibrato I=0.5; fm=10;
```

***doremi.sco***

```shell
#Time; On (8)/Off (9); Channel; Note; Velocity;
#Time; Control; Channel; Effect; On/Off;
0	9	1	60	100
120	8	1	60	100
0   12  1   14  1 #vibrato inicio
40	9	1	62	100
120	8	1	62	100
40	9	1	64	100
120	8	1	64	100
40	9	1	65	100
120	8	1	65	100
40	9	1	67	100
120	8	1	67	100
40	9	1	69	100
120	8	1	69	100
40	9	1	71	100
0   12  1   14  0 #vibrato final
120	8	1	71	100
40	9	1	72	100
120	8	1	72	100
40	0	1	0	0
```

*Luego ejecutamos el programa **synth** como siempre:*

```shell
synth -e effects.orc seno.orc doremi.sco seno_vibrato_normal.wav
```

*A simple vista las señales de la orquestación parecen no tener ningua perturbación o efecto aplicado, pero si miramos al espectro frecuencial, nos vamos a dar cuenta de muchas curiosidades que dan explicación de porqué suena como suena esta grabación con vibrato.*

![Graficas de comparación Waveform Normal vs Waveform + Vibrato](img/DoReMi_Vibrato_FFT_normal.png)

***Imagen generada a partir del código Python en `scripts/vibrato3.py`***

*Si miramos fijadamente, solo la primera y las 2 últimas notas permanecen puras, es decir, no presencian el efecto del vibrato. Esto es fácilmente explicado por el `doremi.sco` que hemos usado, donde podemos ver que solo aplicamos el vibrato a un conjunto intermedio de notas. En cuanto a estas notas que sí tienen perturbación, podemos ver que las representaciones temporales no son muy efectivas para ver los efectos de dicha perturbación. Por eso hemos empleado el uso de la transformada de Fourier, cuya representación sí nos da una mucha mejor visualización de la perturbación provocada por el efecto del vibrato.*

*La primera fila supone la pareja (señal temporal sin tremolo, FFT de dicho señal) mientras que la segunda está diseñada para que haga de contraste con la anterior, donde podemos ver que frecuencialmente existe bastante perturbación. Las demas filas que siguen sirven para ver la peturbación aplicada a cada nota, donde ya deja de existir un afinado y bien definido pico frecuencial (como debería ser según la teoría) sino que existe energía en las frecuencias justo vecinas de ese mismo pico, contaminándola frecuencialmente.*

![Comparación Espectograma Vibrato Normal](img/audio_comparison_vibrato_normal.png)

*En el espectrograma, podemos observar que la frecuencia de cada nota "vibra" alrededor de su valor central, lo que es una característica distintiva del efecto vibrato. Esto se debe a la modulación periódica de la frecuencia, que hace que la frecuencia instantánea de la señal varíe continuamente.*


### *Vibrato Agresivo*

*El Vibrato Agresivo se diferencia por tener valores más altos de frecuencia de modulación (fm) y desviación (I). En este caso, hemos configurado fm=200Hz e I=24, lo que produce un efecto mucho más pronunciado y evidente en la señal de audio.*

**effects.orc**

Hemos añadido la siguiente línea de metadatos:

```shell
14  Vibrato I=24; fm=200;
```

**doremi.sco**

El archivo `doremi.sco` es el mismo que el utilizado para el Vibrato Normal.

Luego ejecutamos el programa **synth** como siempre:

```shell
synth -e effects.orc seno.orc doremi.sco seno_vibrato_agresivo.wav
```

*Al escuchar atentamente el archivo resultante, la modulación más rápida (fm=200Hz) y la mayor desviación (I=24) hacen que las frecuencias de las notas varíen de manera mucho más agresiva, lo que se traduce en un sonido más vibrante e inestable.*

![Graficas de comparación Waveform Normal vs Waveform + Vibrato](img/DoReMi_Vibrato_FFT_agresivo.png)

*En la FFT, se observa una mayor dispersión de energía de las frecuencias centrales de cada nota. A diferencia del Vibrato Normal, donde la frecuencia central vibra alrededor de un punto, en el Vibrato Agresivo aparecen armónicos alejados de la frecuencia central. Estos armónicos indican que la señal está experimentando modulación a frecuencias mucho más altas, produciendo componentes de frecuencia adicionales que se distancian de la frecuencia original de la nota. Esto resulta en una representación frecuencial mucho más compleja y dispersa.*

![Comparación Espectograma Vibrato Agresivo](img/audio_comparison_vibrato_agresivo.png)

*En el espectrograma, esta modulación agresiva se manifiesta en la aparición de bandas adicionales que representan los armónicos producidos por la modulación agresiva. Estos armónicos están más alejados de las frecuencias centrales, indicando un mayor grado de perturbación. En lugar de una vibración suave alrededor de una frecuencia central, el espectrograma muestra un conjunto de frecuencias adicionales que se extienden lejos de la frecuencia principal de la nota, haciendo que el sonido sea percibido como más caótico y desorganizado.*

- Si ha generado algún efecto por su cuenta, explique en qué consiste, cómo lo ha implementado y qué resultado ha producido. Incluya, en el directorio `work/ejemplos`, los ficheros necesarios para apreciar el efecto, e indique, a continuación, la orden necesaria para generar los ficheros de audio usando el programa `synth`.

*Hemos hecho la implementación del efecto llamado **fuzz**. A continuación está su presentación:*

---
---

## *Fuzz*

*El efecto **fuzz** es un tipo de distorsión de audio que produce un sonido muy característico y agresivo. Este efecto se utiliza frecuentemente en la música rock y otros géneros para añadir un tono áspero y sucio a la señal de audio. A diferencia de la distorsión más suave que se podría obtener con un overdrive o una saturación, el fuzz es mucho más pronunciado y se caracteriza por su alta ganancia y la compresión de la señal.*

*Para implementar el efecto fuzz, hemos diseñado un algoritmo que modifica la señal de entrada de la siguiente manera:*

1. **Ganancia (gain):** *Se amplifica la señal de entrada para aumentar su amplitud antes de aplicar la distorsión.*
2. **Curva de transferencia:** *Se utiliza una función tangente hiperbólica (tanh) para comprimir la señal, lo que introduce la distorsión característica del fuzz.*
3. **Mezcla (mix):** *La señal distorsionada se mezcla con la señal original para mantener algo de su carácter original.*
4. **Damping de alta frecuencia (hf_damp):** *Se aplica un factor de amortiguación para reducir las frecuencias altas, lo que suaviza un poco la distorsión.*

**effects.orc**

*Hemos añadido la siguiente línea de metadatos:*

```shell
12  Fuzz
```

**doremi.sco**

*El archivo `doremi.sco` contiene las siguientes instrucciones para aplicar el efecto fuzz:*

```shell
#Time; On (8)/Off (9); Channel; Note; Velocity;
#Time; Control; Channel; Effect; On/Off;
0	9	1	60	100
120	8	1	60	100
0   12  1   12  1 #fuzz inicio
40	9	1	62	100
120	8	1	62	100
40	9	1	64	100
120	8	1	64	100
40	9	1	65	100
120	8	1	65	100
40	9	1	67	100
120	8	1	67	100
40	9	1	69	100
120	8	1	69	100
40	9	1	71	100
0   12  1   12  0 #fuzz final
120	8	1	71	100
40	9	1	72	100
120	8	1	72	100
40	0	1	0	0
```

*Luego ejecutamos el programa **synth** para generar el archivo de audio con el efecto aplicado:*

```shell
synth -e work/effects.orc work/seno.orc work/doremi.sco work/audio_con_fuzz.wav
```

*En el espectrograma del audio con el efecto fuzz, se puede observar que la señal original ha sido significativamente alterada. A diferencia de los efectos de vibrato y tremolo, que modulan la frecuencia o la amplitud de la señal original, el fuzz introduce armónicos y distorsión en la señal, resultando en un espectro de frecuencia mucho más complejo. Esto se traduce en un sonido más agresivo y áspero, con una amplia gama de frecuencias adicionales que se extienden alrededor de la frecuencia central de cada nota.*

![Comparación Espectograma Fuzz](img/audio_comparison_fuzz.png)

*En el espectrograma, esta dispersión de frecuencias se manifiesta como bandas más anchas y ruidosas alrededor de las frecuencias fundamentales de las notas. Esto da como resultado un sonido más lleno y rico, aunque menos puro y afinado. La distorsión característica del fuzz es evidente en la forma en que la energía se distribuye a lo largo del espectro, mostrando la complejidad y el caos introducidos por este efecto.*

*A nivel temporal, la distorsión y saturación de las notas se deben principalmente al proceso de generación de armónicos no lineales introducido por el efecto fuzz. Cuando una señal de audio se distorsiona, las ondas sinusoidales puras que representan las notas musicales se transforman en formas de onda más complejas y ricas en armónicos. Estos armónicos adicionales no están alineados armónicamente con la frecuencia fundamental de la nota original, lo que resulta en una forma de onda que cambia su estructura temporal.*

*En algunas notas, la distorsión puede manifestarse como una amplificación excesiva de ciertos armónicos, dando lugar a una saturación muy perceptible en la señal, tal y como vemos en la imagen. Esto se traduce en un aumento abrupto en la amplitud de la señal en esos armónicos, lo que resulta en una pérdida de definición y claridad en la nota original.*

---
---

### Síntesis FM.

- Construya un instrumento de síntesis FM, según las explicaciones contenidas en el enunciado y el artículo de [John M. Chowning](https://web.eecs.umich.edu/~fessler/course/100/misc/chowning-73-tso.pdf). El instrumento usará como parámetros **básicos** los números `N1` y `N2`, y el índice de modulación `I`, que deberá venir expresado en semitonos.

*Para construir un instrumento de síntesis FM según las especificaciones dadas, vamos a seguir el enfoque basado en la fórmula de frecuencia modulada (FM) propuesta por John M. Chowning. Utilizaremos los parámetros básicos `N1`, `N2` e `I` (índice de modulación expresado en semitonos) para generar varios tipos de sonidos, incluyendo un vibrato y sonidos tipo clarinete y campana. Además, generaremos escalas diatónicas con estos sonidos y guardaremos los resultados en archivos de audio.*

- Use el instrumento para generar un vibrato de *parámetros razonables* e incluya una gráfica en la que se vea, claramente, la correspondencia entre los valores `N1`, `N2` e `I` con la señal obtenida.

### *Implementación del Vibrato con Síntesis FM*

## *Fórmula de Síntesis FM*

*La fórmula para la síntesis de frecuencia modulada (FM) se define como:*

![Formula Señal Sintetizado con Síntesis FM](img/formulaFM.png)

*El parámetro `d`, dentro de la definición del `índice de modulación` (modulation index), es el valor de `peak deviation` o `desviación máxima` de la frecuencia instantáneo de la central (la que se modula). La magia de dicha modulacíon de frecuencia se encuentra en los distintos efectos y relaciones que tienen entre sí los distintos parámetros que parametrizan dicha modulación de frecuencia.*

*Si definimos a α (alpha) como la frecuencia de portadora y a β (beta) como la frecuencia moduladora, el cociente entre las 2, definido como:*

**α/β = N1/N2**

*da lugar a aspectos del espectro de instrumentos modulados interesantes. En concreto, si dicho cociente resulta en una fracción racional, como ahora 10/7 o 13/5 (máximo común divisor es 1), el instrumento resultante contiene contenido espectral harmónico, como el de la siguiente figura:*

![Ejemplo de espectro harmónico](img/espectro_harmonico.png)
*Figura extraída del artículo de `John M. Chowning`*

*Haciendo resumen, para dos valores dados de `N1` y `N2`, junto con la frecuencia central de la nota a tocar, tenemos definida la frecuencia de modulación `fm`. La influencia de dicha `fm` vendrá dada por la amplitud de modulación, dada por el parámetro `I`. Por lo tanto, para poder generar un instrumento del tipo FM, hay que saber:*

  - *N1*
  - *N2*
  - *f0 (frecuencia central o de portadora)*
  - *I (índice de modulación)*

*Procedemos a la implementación de este instrumento básico de síntesis FM. En el mismo artículo de `John M. Chowning` nos ofrece una implementacíon:*

![Implementación de un instrumento de síntesis FM básico](img/SenoFM_simple.png)

*Podemos ver que para la generación de un determinado instrumento mediante síntesis FM básica, hay que disponer de los 4 parámetros de entrada (situados en la parte superior de la figura). Estos parámetros son los que es extraen del diccionario `KeyValue kv(param)` en constructor de dicho instrumento (en parte, ya que algunos parámetros son deducidos a partir de otros, referirse a la fórmulas para su correcta interpretación).*

## Implementación en C++

*Para la implementación del instrumento de síntesis FM, se ha tenido que implementar de nuevo los 3 métodos que definen a un instrumento cualquiera, igual como hicimos con los instrumentos anteriores:*

***Constructor SenoFM()***

```cpp
// Constructor initializes the ADSR envelope and sets default parameters.
SenoFM::SenoFM(const std::string &param)
    : adsr(SamplingRate, param)
{
    bActive = false;
    x.resize(BSIZE);

    /*
      Use KeyValue class to parse 'param' and configure instrument parameters.
      Refer to keyvalue.h for details.
    */
    KeyValue kv(param);

    // Default value if 'N' is not specified in 'param'.
    if (!kv.to_int("N", N))
        N = 40;

    // Attack, Decay, Sustain, Release parameters for ADSR envelope.
    if (!kv.to_float("ADSR_A", adsr_a))
        adsr_a = 0.1;

    if (!kv.to_float("ADSR_D", adsr_d))
        adsr_d = 0.05;

    if (!kv.to_float("ADSR_S", adsr_s))
        adsr_s = 0.5;

    if (!kv.to_float("ADSR_R", adsr_r))
        adsr_r = 0.1;

    // Modulation index 1.
    if (!kv.to_float("I1", I1))
        I1 = 1;

    // Default values for N1 and N2.
    if (!kv.to_float("N1", N1))
        N1 = 1;

    if (!kv.to_float("N2", N2))
        N2 = 1;

    // Default envelope for additional parameters.
    if (!kv.to_float("envelope", envelope))
        envelope = 0;

    // Configure ADSR envelope based on 'envelope'.
    if (envelope == -1)
    {
        adsr.set(adsr_a, 0, adsr_s, adsr_r, 1.5F);
    }

    modulation_phase = 0;
    index_sensitivity = 0;

    std::string file_name;
    static string kv_null;
    waveform_table.resize(N);
    float phase = 0, step = 2 * M_PI / (float)N;
    index = 0;
    for (int i = 0; i < N; ++i)
    {
        waveform_table[i] = sin(phase);
        phase += step;
    }
}
```

***Command()***
```cpp
// Process commands to start, sustain, or release a note.
void SenoFM::command(long cmd, long note, long vel)
{
    if (cmd == 9)
    { //'Key' pressed: trigger attack phase
        bActive = true;
        adsr.start();
        float f0note = pow(2, ((float)note - 69) / 12) * 440; // Convert note to frequency (Hz)
        N_notes = 1 / f0note * SamplingRate;                    // Note period in samples
        index_step = (float)N / N_notes;                        // Table step per note period

        // Reset counters/phases
        index = 0;
        index_sensitivity = 0;
        modulation_phase = 0;
        decay_count = 0;
        decay_count_I = 0;

        fm_modulation = f0note * N2 / N1;                         // Modulating frequency
        phase_step_size = 2 * M_PI * fm_modulation / SamplingRate; // Step of the modulating sine wave

        note_int = round(N_notes);
        temp.resize(note_int);

        if (vel > 127)
            vel = 127;

        A = vel / 127.;
    }
    else if (cmd == 8)
    { //'Key' released: trigger release phase
        adsr.stop();
    }
    else if (cmd == 0)
    {
        // Faster release, ensuring smooth transition
        adsr.set(adsr_s, adsr_a, adsr_d, adsr_r / 4, 1.5F);
        adsr.stop();
    }
}
```

***Synthesize()***

```cpp
// Synthesize the waveform using FM synthesis with ADSR envelope modulation.
const vector<float> &SenoFM::synthesize()
{
    if (not adsr.active())
    {
        x.assign(x.size(), 0);
        bActive = false;
        return x;
    }
    else if (not bActive)
        return x;

    unsigned int index_floor, next_index; // Interpolation indexes
    float weight, weight_fm;              // Interpolation weights
    int index_floor_fm, next_index_fm;    // Frequency interpolation indexes
    std::vector<float> I_array(x.size()); // Array for modulation index I

    // Initialize I_array with user-input modulation index (constant)
    for (unsigned int i = 0; i < x.size(); i++)
    {
        I_array[i] = I2;
        // Apply exponential envelope if selected
        if (envelope > 0)
            I_array[i] = I_array[i] * pow(envelope, decay_count_I);
    }

    // Fill temp with one period of the new signal
    for (unsigned int i = 0; i < (unsigned int)note_int; ++i)
    {

        // Check if floating point index is out of bounds
        if ((long unsigned int)floor(index) > waveform_table.size() - 1)
            index = index - floor(index);

        // Obtain integer index
        index_floor = (int)floor(index);
        weight = index - index_floor;

        // Adjust interpolation indexes if necessary
        if (index_floor == (unsigned int)N - 1)
        {
            next_index = 0;
            index_floor = N - 1;
        }
        else
        {
            next_index = index_floor + 1;
        }
        // Interpolate table values
        temp[i] = ((1 - weight) * waveform_table[index_floor] + (weight)*waveform_table[next_index]);
        // Update real index
        index = index + index_step;
    }

    // Modulate the signal
    for (unsigned int i = 0; i < x.size(); ++i)
    {
        // Check if floating point index is out of bounds
        if (index_sensitivity < 0)
        {
            index_sensitivity = N_notes + index_sensitivity;
        }
        if ((int)floor(index_sensitivity) > note_int - 1)
        {

            index_sensitivity = index_sensitivity - (note_int - 1);
        }
        // Obtain integer index
        index_floor_fm = floor(index_sensitivity);
        weight_fm = index_sensitivity - index_floor_fm;

        // Adjust interpolation indexes if necessary
        if (index_floor_fm == note_int - 1)
        {
            next_index_fm = 0;
            index_floor_fm = note_int - 1;
        }
        else
        {
            next_index_fm = index_floor_fm + 1;
        }
        // Interpolate table values
        x[i] = A * ((1 - weight_fm) * temp[index_floor_fm] + weight_fm * (temp[next_index_fm]));

        // Update real index (phase) and modulated phase
        index_sensitivity = index_sensitivity + 1 - I_array[i] * sin(modulation_phase);
        modulation_phase = modulation_phase + phase_step_size;
    }

    while (modulation_phase > M_PI)
        modulation_phase -= 2 * M_PI;

    // Apply exponential or ADSR envelope modulation
    for (unsigned int i = 0; i < x.size(); i++)
    {
        if (envelope != 0)
        {
            if (envelope > 0) // Exponential decay based on 'envelope'
            {
                x[i] = x[i] * pow(envelope, decay_count);
                decay_count++;
            }
            else if (adsr.active() && envelope == -1)
            {
                x[i] = x[i] * adsr_s; // Adjust level to prevent attack overshoot
            }
        }
    }
    if (envelope <= 0)
        adsr(x); // Apply envelope to x and update ADSR internal state
    return x;
}
```

***getInterpolatedValue()***

```cpp
float SenoFMSimple::getInterpolatedValue(const float phas, string table)
{
    int tbl_size;
    std::vector<float> *tbl;
    if (table == "signal_table")
    {
        tbl_size = tbl_signal.size();
        tbl = &tbl_signal;
    }
    else
    {
        tbl_size = tbl_modulation.size();
        tbl = &tbl_modulation;
    }

    size_t lowerIndex = static_cast<size_t>(std::floor(phas));
    size_t upperIndex = static_cast<size_t>(std::ceil(phas));

    // Boundary conditions for lowerIndex and upperIndex
    if (lowerIndex >= tbl_size || upperIndex >= tbl_size)
    {
        lowerIndex = tbl_size - 1;
        upperIndex = 0;
    }

    // Interpolate between tbl[lowerIndex] and tbl[upperIndex]
    float lowerValue = (*tbl)[lowerIndex];
    float upperValue = (*tbl)[upperIndex];

    // compute interpolation weights
    float interval_length = upperIndex - lowerIndex;
    float lower_index_weight = (upperIndex - phas) / interval_length;
    float upper_index_weight = (phas - lowerIndex) / interval_length;

    // computation of interpolated value
    float interpolated_value = lower_index_weight * lowerValue + upper_index_weight * upperValue;

    return interpolated_value;
}
```
*Dicho método **getInterpolatedValue()** no es nada más que un método adicional que inteligentemente interpola entre valores de una tabla determinada.*

*Ha sido a través de esta implementación que hemos podido generar nuestros primeros sonidos de generación FM natural. A continuación enseñamos algunas gráficas para ejemplificar visualmente la relación existente entre los parámetros básicos de cualquier instrumento de síntesis FM (N1, N2 e I):*

![Comparación Espectro Clarinete con poca vs con más modulación](img/Note_1_FFT_Comparison.png)

*Aquí se compara el espectro de 2 instrumentos de clarinete, uno con índice de modulación `I` y parámetro `N2` más bajos, que deberia proporcionar, teoricamente, menos energia para los harmónicos vs el instrumento pero con parámetros de modulación frecuencial más potentes (`I=3, N2=4`). Ambos instrumentos estan tocando la nota 60, que corresponde a unos 261 Hz, que es precisamente donde encontramos el pico mayor. La presencia de harmónicos, con más o menos potencia, es función ya de los demás parámetros.*

*Como la FFT en **azul** corresponde a una baja modulación frecuencial (sus parámetros son pequeños en comparación con la otra modulacíon) resulta que más porcentaje de la energia espectral reside en dicho pico o frecuencia central, mientras que con el aumento del índice de modulación `I` ocurre una dispersión de la energía hacia otras bandas o regiones espectrales, dando lugar a mayor riqueza frecuencial y sonidos más espectaculares.  No se han podido graficar todos los harmónicos en esta única imagen, pero la cola de harmónicos extendería más lejos (el conocido tren de deltas) para los instrumentos con parámetros de modulación más fuertes, que en este caso resulta ser el instrumento cuya FFT está pintada en rojo.*

- Use el instrumento para generar un sonido tipo clarinete y otro tipo campana. Tome los parámetros del sonido (N1, N2 e I) y de la envolvente ADSR del citado artículo. Con estos sonidos, genere sendas escalas diatónicas (fichero `doremi.sco`) y ponga el resultado en los ficheros `work/doremi/clarinete.wav` y `work/doremi/campana.work`.

### Generación de Sonidos y Escalas Diatónicas

*Para generar los sonidos tipo clarinete y campana, utilizaremos los parámetros especificados en el artículo de Chowning para cada tipo de sonido, incluyendo las envolventes ADSR adecuadas.*

*Mencionar también que para la implementación más compleja y asimismo más completa y correcta de distintos instrumentos de modulación FM hay que modificar el esquema de implementación, de manera que ahora el más avanzado tiene el siguiente aspecto:*

![Implementación de un instrumento de síntesis FM avanzado](img/SenoFM_avanzado.png)

*Mediante esta implementación, seremos capaces de producir instrumentos con aún más riqueza espectral y que encima es dinámica y variante con el tiempo, mediante la varianza de las envolventes de la onda portadora y el índice de modulación `I`.*

#### *Generacíon Clarinete*

*Para la generación del instrumento tipo Clarinete, que es un instrumento del tipo "woodwind", hay que usar valores de la frecuencia central múltiplos enteros de la frecuencia moduladora, es decir, obtener relaciones de N1/N2 del tipo 2/1, 3/1, etc. Nosotros usamos los siguientes parámetros:*

##### *seno.sco* para clarinete

```shell
# Clarinete
4	SenoFM	ADSR_A=0.13; ADSR_D=0.8; ADSR_S=0.3; ADSR_R=0.7; N=40; I=1; I1=0; I2=3; N2=1; N1=1; setting=0; 
```

#### *Generación Campana*

*Para la generación del instrumento tipo campana, que es de la familia de instrumentos **percusivos**, entre muchas otras características, estos instrumentos presentan una envolvente del intervalo de **decaída** de tipo `exponencial` y es por eso que en el fichero `.sco` hemos subministrado dicho instrumento con un parámetro llamado `envelope`:*

```shell
# Campana
3	SenoFM  ADSR_A=0.2; ADSR_D=0.1; ADSR_S=0.3; ADSR_R=0.3; N=40; I=1; I1=0; I2=1.5; N2=15; N1=1; envelope=0.9999; 
```

### *Archivos de Escalas Diatónicas*

Una vez generados los sonidos, generaremos escalas diatónicas utilizando el archivo `doremi.sco` y los sonidos especificados:

#### *Generación de Archivos de Audio*

Una vez definidos los archivos `doremi.sco` con las escalas diatónicas, podemos usar el programa `synth` para generar los archivos de audio `clarinete.wav` y `campana.wav`:

```bash
synth work/seno.orc work/doremi.sco work/clarinete.wav  # Segunda línea del seno.orc
synth work/seno.orc work/doremi.sco work/campana.wav    # Tercera línea del seno.orc
```

  * También puede colgar en el directorio work/doremi otras escalas usando sonidos *interesantes*. Por ejemplo, violines, pianos, percusiones, espadas láser de la
	[Guerra de las Galaxias](https://www.starwars.com/), etc.

  [Escuchar "Clarinete"](work/clarinete.wav)

  [Escuchar "Campana"](work/campana.wav)

---
---

### Orquestación usando el programa synth.

Use el programa `synth` para generar canciones a partir de su partitura MIDI. Como mínimo, deberá incluir la
*orquestación* de la canción *You've got a friend in me* (fichero `ToyStory_A_Friend_in_me.sco`) del genial
[Randy Newman](https://open.spotify.com/artist/3HQyFCFFfJO3KKBlUfZsyW).

- En este triste arreglo, la pista 1 corresponde al instrumento solista (puede ser un piano, flautas,
  violines, etc.), y la 2 al bajo (bajo eléctrico, contrabajo, tuba, etc.).
- Coloque el resultado, junto con los ficheros necesarios para generarlo, en el directorio `work/music`.
- Indique, a continuación, la orden necesaria para generar la señal (suponiendo que todos los archivos
  necesarios están en directorio indicado).

    #### 1. "You've Got a Friend in Me" (Toy Story)

    *Esta canción de Randy Newman se orquesta de la siguiente manera:*

    - Pista 1: Instrumento solista (Clarinete)
    - Pista 2: Bajo (Campana)

    *Se generará el archivo de salida `A_Friend_in_me.wav` con los archivos necesarios en `work/music`.*

    *Orden para generar la señal:*

    ```bash
    synth work/music/orquesta_toy_story.orc work/music/ToyStory_A_Friend_in_me.sco work/music/A_Friend_in_me.wav
    ```

    *Para escuchar la canción completa, haz clic en el siguiente enlace:*

    [Escuchar "A Friend in Me"](work/music/A_Friend_in_me.wav)


También puede orquestar otros temas más complejos, como la banda sonora de *Hawaii5-0* o el villacinco de
John Lennon *Happy Xmas (War Is Over)* (fichero `The_Christmas_Song_Lennon.sco`), o cualquier otra canción
de su agrado o composición. Se valorará la riqueza instrumental, su modelado y el resultado final.
- Coloque los ficheros generados, junto a sus ficheros `score`, `instruments` y `efffects`, en el directorio
  `work/music`.
- Indique, a continuación, la orden necesaria para generar cada una de las señales usando los distintos ficheros.

    #### 2. "November Rain"

    *Para esta pieza de Guns N' Roses, se utilizan los siguientes instrumentos:*

    - Pista 1: Piano
    - Pista 2: Vocales
    - Pista 3: Sección de Cuerdas
    - Pista 4: Guitarra líder y rítmica
    - Pista 5: Sección de Cañas
    - Pista 6: Sección de Cuerdas de Respaldo
    - Pista 7: Percusión

    *Orden para generar las señales:*

    ```bash
    midi2sco --bpm 80 work/music/November_rain.mid work/music/November_rain.sco
    synth work/music/orquesta_November_rain.orc work/music/November_rain.sco work/music/November_rain.wav
    ```

    *Para escuchar la canción completa, haz clic en el siguiente enlace:*

    [Escuchar "November Rain"](work/music/November_rain.wav)

    #### 3. "Help!" (The Beatles)

    *Para esta canción de The Beatles, se usan los siguientes instrumentos:*

    - Pista 1: Piano
    - Pista 2: Vocales
    - Pista 3: Sección de Cuerdas
    - Pista 4: Guitarra líder y rítmica
    - Pista 5: Sección de Cañas
    - Pista 6: Sección de Cuerdas de Respaldo
    - Pista 7: Percusión

    *Se han creado dos versiones ligeramente diferentes de la orquestación de "Help!" para explorar distintas interpretaciones sonoras. La primera versión se enfoca en mantener una percusión más prominente y definida, utilizando ajustes estándar para los instrumentos. En contraste, la segunda versión busca un enfoque más suave, con una percusión más sutil y ajustes específicos en el tiempo de decaimiento de los instrumentos, lo cual altera el ritmo y la dinámica general de la canción.*

    *Orden para generar las señales:*

    ```bash
    midi2sco --bpm 192 work/music/Help.mid work/music/Help.sco
    synth work/music/orquesta_Help.orc work/music/Help.sco work/music/Help.wav
    ```

    *Para escuchar la canción completa, haz clic en el siguiente enlace:*

    [Escuchar "Help"](work/music/Help.wav)

    [Escuchar "Help (Alternative version)"](work/music/Help2.wav)


    #### Detalles adicionales

    *Cada instrumento ha sido ajustado seleccionando los parámetros en base al tipo de sonido deseado y las características específicas de cada canción. Este proceso asegura que cada instrumento contribuya de manera armoniosa al conjunto musical, manteniendo una coherencia estilística y expresiva en toda la composición.*

    *Se ha puesto un énfasis especial en la riqueza instrumental, garantizando que cada instrumento no solo cumpla su función melódica o armónica, sino que también añada textura y profundidad al arreglo general. Esperamos que, de este modo, nuestro oyente disfrute al máximo de su experiencia auditiva, sumergiéndose en una interpretación musical enriquecedora y envolvente.*

---
---