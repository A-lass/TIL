# JVM, JRE, JDK
### JVM (Java Virtual Machine)
* 자바 가상 머신으로 자바 바이트코드(`.class 파일`)를 OS에 특화된 코드로 변환(인터프리터, JIT 컴파일러)하여 실행한다.
* 바이트코드를 실행하는 표준이자 구현체 (세부 구현은 vendor에 따라 다름)
* 특정 플랫폼에 **종속적**이다 -> 각 플랫폼에 맞는 `JVM`이 있다.
    * 자바는 특정 플랫폼에 **독립적**이다.

### JRE (Java Runtime Environment)
* JVM + Library
* 자바 어플리케이션을 실행할 수 있도록 구성된 배포판
    -> 자바 런타임 환경에서 사용하는 프로퍼티 세팅이나 리소스 파일을 가지고 있다.
* 개발 관련 도구는 제공하지 않는다.
    -> `JDK`에서 제공

### JDK (Java Development Kit)
* `JRE` + 개발에 필요한 툴
* 소스코드를 사용할 때 사용하는 자바 언어는 플랫폼에 독립적이다.
* 오라클은 `Java 11` 부터 `JDK`만 제공하며 `JRE`는 따로 제공하지 않는다.

<br/><br/>

# JVM 구조

![image](https://github.com/A-lass/TIL/assets/84514047/3061c5df-525e-41e5-b999-61cfe76eaa38)

## 클래스 로더 (Class Loader)
![image](https://github.com/A-lass/TIL/assets/84514047/69e16854-3172-42e3-8202-9c5e2c085e7b)

* 로딩 -> 링킹 -> 초기화 순으로 진행된다.
### 로딩 (Loading)
* 클래스를 읽어와 메모리의 **메서드 영역**에 저장한다.
* 메서드 영역에 저장하는 데이터
    * FQCN (Fully Qualified Class Name)
    * 클래스, 인터페이스, Enum
    * 메서드, 변수
* 로딩이 끝나면 해당 클래스 타입의 Class 객체를 생성하여 **힙 영역**에 저장한다.
### 링킹 (Linking)
* 코드의 레퍼런스를 연결한다.
* Verify -> Prepare -> Resolve(Optional) 순으로 진행된다.
    * Verify : `.class` 파일이 유효한지 검증
    * Prepare : 클래스 변수(`static` 변수)와 기본값에 필요한 메모리를 준비
    * Resolve : 심볼릭 메모리 레퍼런스를 메서드 영역에 있는 실제 레퍼런스로 교체
### 초기화 (Initialization)
* `static` 변수를 초기화 하고, `static` 블록을 실행하여 클래스의 상태를 초기화한다.

<br/>

## 메모리 (Runtime Data Area)
### 메서드 (Method Area)
* 클래스 수준의 정보 *(클래스 이름, 부모 클래스 이름, 메서드, 변수 등)* 가 저장된다.
* 모든 스레드가 **공유**하는 영역

### 스택 (Stack Area)
* **스레드마다** 런타임 스택을 만들고, 그 안에 메서드 호출을 스택 프레임으로 쌓는다.
* 스레드가 종료되면 런타임 스택도 사라진다.

### 힙 (Heap Area)
* `new` 키워드로 생성되는 객체와 배열이 할당되는 공간
* 메서드 영역에 저장되어 있는 클래스만 생성 가능
* `GC` 가 참조되지 않는 메모리를 확인하고 제거하는 영역
* 모든 스레드가 **공유**하는 영역

### PC Register
* 스레드가 시작될 때 생성되며 **스레드마다** 하나씩 존재한다.
* 스레드 내 현재 실행할 스택 프레임을 가리키는 포인터를 생성한다.

### Native Method Stack
* 자바 외 언어로 작성된 네이티브 코드가 저장되는 공간

<br/>

## 실행 엔진 (Execution Engine)
### 인터프리터 (Interpreter)
* 바이트코드를 한 줄씩 실행한다.
### JIT 컴파일러 (Just-In-Time Compiler)
* 효율을 높이기 위해 인터프리터가 반복되는 코드를 발견하면 JIT 컴파일러로 반복되는 코드를 모두 네이티브 코드로 바꿔둔다.
    이후 인터프리터는 네이티브 코드로 컴파일된 코드를 바로 사용한다.
### GC (Garbage Collector)
* 더 이상 참조되지 않는 객체를 모아서 정리한다.

<br/>

## JNI (Java Native Interface)
* 자바 어플리케이션에서 C, C++, 어셈블리로 작성된 함수를 사용할 수 있도록 하는 방법을 제공한다.
* `native` 키워드를 사용하여 메서드를 호출한다.

<br/>

## 네이티브 메서드 라이브러리 (Native Method Library)
* C, C++ 로 작성된 라이브러리



### Ref.
[더 자바, 코드를 조작하는 다양한 방법](https://www.inflearn.com/course/the-java-code-manipulation/dashboard)