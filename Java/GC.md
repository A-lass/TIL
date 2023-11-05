# GC (Garbage Collection)
* 자바에서는 메모리를 `GC`라는 알고리즘을 통하여 관리한다. 
* 더 이상 사용하지 않는 객체를 효과적으로 처리하는 작업을 `GC`라고 한다.
* `JVM`의 메모리 영역(Runtime Data Area) 중 `GC`가 발생하는 부분은 **힙 영역**이다.

<br/><br/>

# Runtime Data Area
![image](https://github.com/A-lass/TIL/assets/84514047/6f928ebc-e33b-45a6-a09b-816919ec7cc9)
## Heap 메모리
### 힙 영역(Heap Area)
* 클래스의 인스턴스, 배열이 쌓이는 영역
* **공유** 메모리(Shared memory)라고도 불리우며 여러 스레드에서 공유하는 데이터들이 저장된다.

<br/>

## Non-heap 메모리
### 메서드 영역(Method Area)
* 모든 JVM 스레드에서 **공유**하는 영역
* 런타임 상수 풀
    * 자바의 클래스 파일에 포함되어 있는 `constant_pool`이라는 정보를 실행 시에 참조하기 위한 영역
    * 실제 상수 값도 여기에 포함될 수 있지만, 실행 시에 변하게 되는 필드 참조 정보도 포함된다.
* 필드 정보에는 메서드 데이터, 메서드와 생성자 코드가 있다.

### 스택 영역(Stack Area)
* 스레드가 시작할 때 런타임 스택이 생성된다. 이 스택에 메서드가 호출되는 정보인 프레임이 저장된다.
* 지역 변수, 임시 결과, 메서드 수행과 리턴에 관련된 정보들도 포함된다.

### Native Method Stack
* 자바 코드가 아닌 다른 언어로 된 코드들이 실행하게 될 때의 스택 정보를 관리한다.

### PC Register
* 자바의 스레드들은 각자의 PC(Program Counter)를 갖는다.
* 네이티브한 코드를 제외한 모든 자바 코드들이 수행될 때 JVM의 인스트럭션 주소를 `PC Register`에 보관한다.

<br/>

* **힙 영역**과 **메서드 영역**은 JVM이 시작될 때 생성된다.

<br/><br/>

# GC의 원리와 종류
* `GC` 작업을 하는 가비지 컬렉터는 다음의 역할을 한다.
    * 메모리 할당
    * 사용 중인 메모리 인식
    * 사용하지 않는 메모리 인식

<br/>

* `GC`는 크게 `Minor GC`와 `Major GC`로 나뉜다.
    * `Minor GC` : `Young` 영역에서 발생하는 `GC`
    * `Major GC` : `Old` 영역에서 발생하는 `GC`
    * 이 두 가지 GC가 어떻게 상호 작용하느냐에 따라 `GC` 방식에 차이가 난다.

<br/>

* 힙 영역은 크게 `Young`, `Old` 두 영역으로 나뉘며 `Young` 영역은 다시 `Eden` 영역 및 두 개의 `Survivor` 영역으로 나뉜다.
![image](https://github.com/A-lass/TIL/assets/84514047/8f62c877-f757-4ca2-a328-ba22e6ba51df)

### 원리
* 일단 메모리에 객체가 생성되면 `Eden`에 객체가 지정된다.
* `Eden` 영역에 데이터가 꽉 차면, 이 영역에 있던 객체가 어디론가 옮겨지거나 삭제되어야 한다. 이 때 옮겨가는 위치가 `Survivor` 영역이다.
* 두 개의 `Survivor` 영역 사이에 우선 순위가 있는 것은 아니며, 이 두 개 의 영역 중 한 영역은 반드시 비어 있어야 한다.
    그 비어 있는 영역에 `Eden` 영역에 있던 객체 중 `GC` 후 살아 남은 객체들이 이동한다. 
    이와 같이 `Eden` 영역에 있던 객체는 `Survivor` 영역의 둘 중 하나에 할당된다.
* 객체가 영역을 옮길 때 마다 `age-bit`가 1씩 증가한다.
* 할당된 `Survivor` 영역이 차면, `GC`가 되면서 `Eden` 영역에 있는 객체와 꽉 찬 `Survivor` 영역에 있는 객체가 비어있는 `Survivor` 영역으로 이동한다. 
이러한 작업을 반복하면서, `Survivor 0과 1`를 왔다 갔다 하면서 일정 수준의 `age-bit`를 넘긴 객체들은 `Old` 영역으로 이동한다(**Promotion**).
* 객체의 크기가 아주 큰 경우 `Young` 영역에서 `Survivor` 영역을 거치지 않고 바로 `Old` 영역으로 이동하는 경우가 있을 수 있다.

<br/>

* `GC가` 발생하거나 객체가 각 영역에서 다른 영역으로 이동할 때 어플리케이션의 병목이 발생하면서 성능에도 영향을 주게 된다.
* `핫 스팟 JVM`에서는 **스레드 로컬 할당 버퍼(TLABs:Thead-Local Allocation Buffers)** 라는 것을 사용하여 다른 스레드에 영향을 주지 않는 메모리 할당 작업이 가능해진다.

<br/><br/>

# GC 알고리즘
> Root Space ? 
> * `Stack`의 로컬 변수
> * `Method Area`의 `static` 변수
> * `Native Method Stack`의 `JNI` 참조
### Reference Counting
![image](https://github.com/A-lass/TIL/assets/84514047/89a26519-c3d1-4e65-848d-d5a72eba9dae)
* 알고리즘
    * 객체를 가리키는 포인터의 수만큼 카운트를 유지한다. 이 카운트는 객체의 참조 변수가 생성되거나 파괴됨에 따라 증가하거나 감소한다.
    * 객체의 참조 카운트가 0이 되면 해당 객체는 제거된다.
* 단점
    * 순환 참조 문제가 발생할 수 있다.

<br/>

### Mark-and-Sweep
![image](https://github.com/A-lass/TIL/assets/84514047/664095c0-e8af-46d1-bf68-afddf788b093)
* 자바에서 사용되는 메모리 관리 방식
* Reference Counting 알고리즘의 순환 참조 문제를 해결할 수 있다.
* 알고리즘
    * Step 1) **Mark**
        * root space 에서 시작해 메모리 그래프를 추적하여 접근 가능한 객체들을 `mark` 한다. 
    * Step 2) **Sweep**
        * 연결되지 않는 객체들을 모두 지운다
        * 이 과정을 통해 root space 와 연결되지 않은 순환 참조를 하는 객체들을 제거할 수 있다.
    * Step 3) **Compaction (Optional)**
        * 살아남은 객체들을 메모리 영역의 한 쪽으로 정리한다.
        * 이를 통해 메모리 파편화를 방지할 수 있다.
* 단점
    * 의도적으로 `GC`를 실행시켜야 한다.
    * 어플리케이션 실행과 `GC` 실행이 병행된다.

<br/><br/>

# GC 방식
> Stop The World ?
> * GC를 실행하기 위해 JVM이 어플리케이션의 실행을 멈추는 것
### Serial GC
* 하나의 스레드로 GC를 실행
* Stop The World 시간이 긺
* 싱글 스레드 환경 및 Heap이 매우 작을 때 사용
### Parallel GC
* 여러 개의 스레드로 GC를 실행
* 멀티코어 환경에서 사용
* `Java 8`의 default GC 방식
### CMS GC (Concurrent Mark-Sweep GC)
* Stop The World 최소화를 위해 고안
* GC 작업을 어플리케이션과 동시에 실행
* 메모리 및 CPU 사용량 높음
* Mark-and-Sweep 후 Compaction 기본 제공 X
* G1 GC 등장에 따라 Deprecated

### G1GC (Garbage First Garbage Collector)
* 힙 영역을 `Region`으로 잘게 나누어 어떤 `region`은 `Young Generation`, 어떤 `region`은 `Old Generation`으로 사용한다.
* 런타임에 G1 GC가 필요에 따라 영역 별 `Region` 개수를 튜닝한다.
* `Java 9`부터 default GC 방식

<br/><br/>

# G1 GC 동작 과정
### Young GC
1. 몇 개의 `Region`을 선정하여 `Young Generation`으로 지정한다.
2. 해당 영역에 객체가 생서되면서 데이터가 쌓인다.
3. `Young Generation`으로 할당된 `Region`에 데이터가 꽉 차면 GC를 수행한다.
4. GC를 수행하면서 살아있는 객체들만 `Survivor` 영역으로 이동시킨다.
* 이렇게 살아 남은 객체들이 이동된 구역은 새로운 `Survivor` 영역이 되고, 그 다음에 `Young GC`가 발생하면 `Survivor` 영역에 계속 쌓는다.
* 계속해서 살아남는 객체들은 몇 번의 `aging` 작업 이후 `Old` 영역으로 Promotion 된다.

### Old GC
1. 초기 표시(Initial Mark) 단계 `STW`
    * `Old` 영역에 있는 객체에서 `Survivor` 영역의 객체를 참조하고 있는 객체들을 표시(mark)한다.
2. 기본 구역 스캔(Root region scann) 단계
    * `Old` 영역 참조를 위해서 `Survivor` 영역을 훑는다.
    * 이 작업은 `Young GC`가 발생하기 전에 수행된다.
3. 컨커런트 표시 단계
    * 전체 힙 영역에서 살아있는 객체를 찾는다.
    * 이 때 `Young GC`가 발생하면 잠시 멈춘다.
4. 재표시(Remark) 단계 `STW`
    * 힙에 살아있는 객체들의 표시 작업을 완료한다.
    * snapshot-at-the-beginning (SATB)이라는 알고리즘을 사용한다.
5. 청소(Cleanup) 단계 `STW`
    * 살아있는 객체와 비어 있는 구역을 식별하고, 필요 없는 객체들을 지운다.
    * 그 후 비어 있는 구역을 초기화한다.
6. 복사(Copy) 단계 `STW`
    * 살아있는 객체들을 비어 있는 구역으로 모은다.

<br/><br/>

### Ref.
[이상민, 『개발자가 반드시 알아야 할 자바 성능 튜닝 이야기』, 인사이트(insight), 2013.](https://www.yes24.com/Product/Goods/11261731)  
[[10분 테코톡] 🤔 조엘의 GC](https://www.youtube.com/watch?v=FMUpVA0Vvjw&list=LL&index=30&t=511s&ab_channel=%EC%9A%B0%EC%95%84%ED%95%9C%ED%85%8C%ED%81%AC)  
https://rebelsky.cs.grinnell.edu/Courses/CS302/99S/Presentations/GC/  
https://www.waitingforcode.com/off-heap/on-heap-off-heap-storage/read  
