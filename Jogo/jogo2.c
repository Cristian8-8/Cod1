#include<stdio.h>

void imprimirMapa(char mapa[4][5]) {
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            printf("|%c| ", mapa[i][j]);
        }
        printf("\n");
    }
}

void scanmove(char map[4][5],char move[],int *x_p,int *y_p) {
    map[*x_p][*y_p]=' ';
    if(move[0]=='a' && *y_p>0){
        (*y_p)--;
    }
    else if (move[0]=='d' && *y_p<4){
        (*y_p)++;
    }
    else if(move[0]=='w' && *x_p>0){
        (*x_p)--;
    }
    else if(move[0]=='s' && *x_p<4){
        (*x_p)++;
    }
    map[*x_p][*y_p]='p';    
}

int main(){
    char map[5][5] = {
        {' ', ' ', ' ', ' ',' '},
        {' ', ' ', ' ', ' ',' '},
        {' ', ' ', 'p', ' ',' '},
        {' ', ' ', ' ', ' ',' '},
        {' ', ' ', ' ', ' ',' '}
    };
    char move[4];
    int x_p=2,y_p=2;
    
    while(1){
        printf("\033[H\033[J");
        printf("Posicao atual: Linha %d, Coluna %d\n", x_p, y_p);
        imprimirMapa(map);
        scanf(" %3s",&move);
        scanmove(map,move,&x_p,&y_p);
        
    }
}
