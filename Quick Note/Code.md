Prime number checker
```java
public class MathUtil {
	public static boolean isPrime(int num) {
		if(num < 2){
			return false;
		}
		for(int i=2;i<num;i++){
			if(num%i==0){
				return false;
			}
		}
		return true;
	}
}
```

Factorial Recursion
```java
public class MathUtil {
	public static int factorial(int num) {
		if(num == 1) {
			return 1;
		}
		return num * factorial(num-1);
	}
}
```

Fibonanci Recursion

```java
public class MathUtil {
	public static int fibo(int num) {
		if(num==1 || num==0) {
			return 1;
		}
		return fibo(num-1) + fibo(num-2);
	}	
}
```
