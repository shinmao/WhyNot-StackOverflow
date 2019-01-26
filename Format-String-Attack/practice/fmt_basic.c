#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

void set_buf(){
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
}

int a = 0;    // one global variable

int main(){

    char name[0x60] , secret[0x10] , buf[0x30];
    memset( name , 0 , sizeof( name ) );
    set_buf();
    
    int fd = open( "/dev/urandom" , O_RDONLY ); 
    if( fd < 0 ){ 
        printf("error\n"); 
        _exit(1); 
    }
    read( fd , secret , 0x10 ); 
    close(fd);

    puts( "Hi! Im Uvuvwevwevwe Onyetenyevwe Ugwemuhwem Osass :D" );
    puts( "What's your name ?" );

    read( 0 , name , 0x5f );
    puts( "Hello:" );
    printf( name );    // payload: 

    if( a == 0xfaceb00c ){
        system( "cat /home/lab1/flag" );

        puts( "Do you know my secret :P ?" );
        read( 0 , buf , 0x10 );

        if( !strncmp( buf , secret , 0x10 ) ){
            system( "cat /home/lab1/flag2" );

            puts( "Hello! my friend! Say something to Osass:" );
            memset( buf , 0 , sizeof( buf ) );
            read( 0 , buf , 0x2f );
            puts( "You said:" );
            printf( buf );     // gothijacking
            puts( "Say something again!" );
            memset( buf , 0 , sizeof( buf ) );
            read( 0 , buf , 0x2f );   // send '/bin/sh'
            printf( buf );   // > system('/bin/sh')

        }
        else puts( "You are not my friend :(" );

    }
    else puts( "NOOOOOOOOOOOOOOO :(" );

    return 0;
}
