#include <stdio.h>

void accept(int a[10][10], int m, int n){
	int i,j;
	printf("Enter the values of matrix: \n");
	for(i=0;i<m;i++) {
		for(j=0;j<n;j++) {
			scanf("%d",&a[i][j]);
		}
	}
}

void display(int a[10][10], int m, int n){
	int i,j;
	printf("Displaying matrix: \n");
	for(i=0;i<m;i++) {
		for(j=0;j<n;j++) {
			printf("%d\t",a[i][j]);
		}
		printf("\n");
	}
}

void add(int a[10][10], int b[10][10], int m, int n) {
	int c[10][10],i,j;
	
	for(i=0;i<m;i++) {
		for(j=0;j<n;j++) {
			c[i][j] = a[i][j] + b[i][j];
		}
	}
	display(c,m,n);
}

void sub(int a[10][10], int b[10][10], int m, int n) {
	int c[10][10],i,j;
	
	for(i=0;i<m;i++) {
		for(j=0;j<n;j++) {
			c[i][j] = a[i][j] - b[i][j];
		}
	}
	display(c,m,n);
}

void multiply(int a[10][10], int b[10][10], int m, int n,int y) {
	int i,j,k,c[10][10] = {0};
	for(i=0;i<m;i++) {
		for(j=0;j<n;j++) {
			for(k=0;k<y;k++) {
				c[i][j] += a[i][k] + b[k][j];
			}
		}
	}
	display(c,m,n);
}

void trans(int a[10][10], int m, int n) {
	int c[10][10],i,j;
	
	for(i=0;i<m;i++) {
		for(j=0;j<n;j++) {
			c[i][j] = a[j][i];
		}
	}
	display(c,m,n);
}

int main() {
	int a[10][10], b[10][10], m, n, x, y, ch;
	printf("\n Enter the dimensions of matrix: ");
	scanf("%d%d",&m,&n);
	accept(a,m,n);
	display(a,m,n);
	printf("\n Enter the dimensions of matrix: ");
	scanf("%d%d",&x,&y);
	accept(b,x,y);
	display(b,x,y);
	
	while(1){
		printf("\n1. Addition");
		printf("\n2. Subtraction");
		printf("\n3. Multiplication");
		printf("\n4. Transpose");
		printf("\n5. Exit");
		printf("\nEnter your choice: ");
		scanf("%d",&ch);
		switch (ch){
			case 1:
				if(m==x && n==y){
					add(a,b,m,n);}
				else{
					printf("Invalid Dimension!");}
				break;
			case 2:
				if(m==x && n==y){
					sub(a,b,m,n);}
				else{
					printf("Invalid Dimension!");}
				break;
			case 3:
				if(n==x){
					multiply(a,b,m,n,y);}
				else{
					printf("Invalid Dimension!");}
				break;
			case 4:
				trans(a,m,n);
				break;
			case 5: 
				break;
			
		}
	}
	
	return 0;
}