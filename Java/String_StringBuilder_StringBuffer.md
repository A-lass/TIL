# StringBuilder 와 StringBuffer
자바에서 문자열을 만드는 클래스로 `String`, `StringBuffer`, `StringBuilder` 가 가장 많이 사용된다.
`StringBuffer` 와 `StringBuilder` 에서 제공하는 메서드는 동일하다.

### StringBuffer
* 스레드에 안전하게(ThreadSafe) 설계되어 있으므로, 여러 개의 스레드에서 하나의 StringBuffer 객체를 처리해도 전혀 문제가 되지 않는다.
### StringBuilder
* 단일 스레드에서의 안전성만을 보장하므로 여러 개의 스레드에서 하나의 StringBuilder 객체를 처리하면 문제가 발생한다.

<br/><br/>

# String vs StringBuffer vs StringBuilder
### String 에서 + 연산을 이용한 문자열 더하기

```java
final String val = "abcde";
String str = ""; // 주소 50  :  
str += val;      // 주소 100 : abcde
str += val;      // 주소 150 : abcdeabcde
str += val;      // 주소 200 : abcdeabcdeabcde
```

위 코드처럼 `String` 에 `+` 연산을 하면 새로운 `String` 클래스의 객체가 만들어지고 이전에 있던 `str` 객체는 필요 없는 쓰레기 값이 되어 GC 대상이 된다. 
즉, “abcde”, “abcdeabcde”, “abcdeabcdeabcde” 의 값을 갖는 객체가 각각 모두 다른 객체가 된다는 것이다.
이런 작업이 반복 수행되면 GC 가 많이 발생하여 메모리를 많이 사용하게 되고, 응답 속도에도 많은 영향을 미치게 된다.

<br/>

### StringBuffer, StringBuilder 에서 append() 를 이용한 문자열 더하기

```java
final String val = "abcde";
StringBuilder sb = new StringBuilder(val); // 주소 50 : 
sb.append(val);      // 주소 50 : abcde
sb.append(val);      // 주소 50 : abcdeabcde
sb.append(val);      // 주소 50 : abcdeabcdeabcde
```

`StringBuffer` 나 `StrintBuilder` 는 `String` 과 다르게 새로운 객체를 생성하지 않고, 기존에 있는 객체의 크기를 증가시키면서 값을 더한다.

<br/>

### 그렇다면 언제 String 을 써야하고 언제 StringBuffer 와 StringBuilder 를 사용해야 할까?

- 짧은 문자열을 더할 경우
    
     **→ String**
    
- Thread-Safety 한 프로그램이 필요하거나, 개발 중인 시스템의 부분이 Thread-Safety 한지 모를 경우
    - ex) 클래스에 static 으로 선언한 문자열 변경 or 싱글톤으로 선언된 클래스에 선언된 문자열일 경우
    
    **→ StringBuffer**
    
- Thread-Safety 의 여부와 전혀 관계 없는 프로그램을 개발할 경우
    - ex) 메서드 내에 변수를 선언했을 때
    
    **→ StringBuilder**
    
<br/><br/>

# 정리
- 문자열을 처리하기 위한 `String`, `StringBuffer`, `StringBuilder` 세 가지 클래스 중, 메모리를 가장 많이 차지하고 응답 시간에 많은 영향을 주는 것은 `String` 클래스다.
- 문자열을 더하는 작업이 반복되는 경우, 스레드와 관련이 있으면 `StringBuffer` 를, 스레드 안전 여부와 상관이 없으면 `StringBuilder` 를 사용하자.

<br/><br/>

### Ref.
이상민, 『개발자가 반드시 알아야 할 자바 성능 튜닝 이야기』, 인사이트(insight), 2013.

[https://docs.oracle.com/javase/8/docs/api/java/lang/StringBuilder.html](https://docs.oracle.com/javase/8/docs/api/java/lang/StringBuilder.html)

[https://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html](https://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html)