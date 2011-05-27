

/*  pdspread.c                                    */  
/*  A simple spreadsheet in C                     */ 
/*  Remember to compile this code with the        */ 
/*  -lncurses option. This links it with curses.  */  
/*  This code is released to the public domain.   */ 
/*  "Share and enjoy..."  ;)                      */ 


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <curses.h>


/* Declare our window  */ 
   WINDOW *mywin;  

/* The row and column of the cursor, and the number of */ 
/* rows and cols in the window. */  
int r, c, nrows, ncols;  

/* An array to hold the contents of a line */ 
/* Note - need to make sure that if you insert text which makes the line */
/* longer than 80 chars, then a new line array is created and text added */ 
/* to it. */ 
char text[80];  

/*  Character read from keyboard. */ 
/*  Note - make sure this is an INT variable. */ 
int ch; 

/*  Set insert mode to zero when we start. */ 
int insmode = 0; 

/*  Width of a cell. */  
int width = 7; 

/*  Left boundary  */ 
int lbound = 7; 

/*  Top boundary  */  
int tbound = 2; 


/*  Zip function for two numeric arrays.  */ 
void zip(int *array1, int *array2) 
{ 
    int i ; 
            
    /* Test the array lengths, If they are not equal, only zip up to 
     * the length of the shortest one. */     
    int len1 = sizeof(array1) ;   
    int len2 = sizeof(array2) ;   
     
    /*  Use the shortest array length */  
    int min = len1 < len2 ? len1 : len2 ; 
    
    printf("Len1: %d  Len2: %d  min: %d \n", len1, len2, min ); 
            
    int resarray[min][2];     
    
    int pair[2] ;     
            
         for(i=0; i<min; i++) 
         { 
          
          /* Our pair array */             
          pair[0] = array1[i] ; 
          pair[1] = array2[i] ; 
          
          resarray[i][0] = pair[0] ; 
          resarray[i][1] = pair[1] ; 
          
          /* printf("Result[%d] is (%d,%d) \n", i, resarray[i][0], resarray[i][1]); */ 
          
         }                                 
}; 



/* A data "object" */ 
typedef struct 
{ 
  int value; 
  char align[5]; 
} data;      


/* A cell "object"  */ 
typedef struct 
{   
  int yval; 
  int xval; 
  int ynew; 
  int xnew; 
  int val;       
} cell;  
      
/* A position struct for the cell-pointer. */ 
typedef struct 
{ 
  int ypos; 
  int xpos;       
} pos;     
 
/* Declare a pos for the current position of the cell-pointer. */ 
pos curpos;  


/* A cartesian product function. */ 
void cp(pos pos1, pos pos2) 
{ 
   int xdiff = pos2.xpos - pos1.xpos; 
   int ydiff = pos2.ypos - pos1.ypos;   
  
   /* Declare our array to hold the results.  */  
   int resarray[xdiff][ydiff];   
   
   int x, y;
       
   /* Having the y-loop outside the x-loop means that  */ 
   /* the operation proceeds row-by-row.               */                   
   for (y=pos1.ypos; y<pos2.ypos; y++)   
     for (x=pos1.xpos; x<pos2.xpos; x++)  
          { 
            resarray[x][0] = y;                 
            resarray[x][1] = x; 
            printf("(%d , %d) \n", resarray[x][0], resarray[x][1]);   
          }                                                  
}     
    


/* A sheet "object".  */  
typedef struct 
{ 
  char screen[20]; 
  int ypos;   
  int xpos;   
} sheet;   

/* Declare an instance of a sheet.  */  
sheet mysheet;  


/*  Set the values for a data "object". */  
void setdata(void *val) 
{ 
   data *dp = (data*)val ; 
   printf("%d \n%s", dp->value, dp->align);                   
}  


void setcell(void *val, int y, int x, int ynew, int xnew) 
{ 
   cell *c = (cell*)val ;    
   c->yval = y;  c->xval = x;  c->ynew = ynew; c->xnew = xnew;         
}     


void setcurpos(int y, int x) 
{    
   curpos.ypos = y; 
   curpos.xpos = x;         
}     


pos getcurpos(void) 
{     
   return curpos;
}      



/* Move the cell highlight  */ 
void movecell(int y, int x, char dir) 
{ 
  /* Ensure the direction is in uppercase. */   
  char mydir = toupper(dir);  
  
  /* Get the current values of y and x. */  
  getyx(mywin, r, c);
  curpos.ypos = r; 
  curpos.xpos = c; 
  
  
  /* Declare the new values for x and y. */ 
  int newx, newy;   
      
  if ( (mydir == 'L' ) && (curpos.xpos - width) >= lbound)  
      newx = curpos.xpos - width;   
  if (  mydir == 'R' )  newx = curpos.xpos + width ;
  if ( (mydir == 'U' ) && (curpos.ypos > tbound) )    
      newy = curpos.ypos - 1 ;  
  if ( mydir == 'D' )   newy = curpos.ypos + 1 ;
  if ( mydir == '*' )   
      newx = curpos.xpos;  
      newy = curpos.ypos; 
                           
  /* Remove the highlight from the current cell.  */    
     /* move(curpos.ypos, curpos.xpos);  */       
      mvchgat(curpos.ypos, curpos.xpos, width, A_NORMAL, 0, NULL);         
      refresh(); 
  /* Now move the highlight to the new coordinates.  */                
      /* move(newy, newx);  */       
      mvchgat(newy, newx, width, A_STANDOUT, 0, NULL);  
      refresh();                   
  /*  Get the new coordinates. */     
      getyx(mywin, r, c);
      curpos.ypos = r; 
      curpos.xpos = c;                       
      refresh();       
            
}       
    
    
/* Write some text into a cell  */ 
void writecell(pos cell, char *text) 
{    
   move(curpos.ypos, curpos.xpos);     
   addstr(text);           
   refresh();    
}          
    
    
void writerange(pos cell1, pos cell2, char *text) 
{ 
   char datalist[strlen(text)] ;
   
   /* Create the position list by finding the cartesian product */
   /* of cell1 and cell2.  */ 
    

   self.poslist = poslist  
   
   # Get the position of the cursor. 
   (y, x) = self.scr.getyx() 
   
   # Write the text 
   for x,y in zip(self.datalist, self.poslist): 
      self.scr.addstr(y[0], y[1], str(x) ) 
   
   # Refresh the screen 
   self.scr.refresh()                                                                  
                       
}         
    
       
       
void makesheet(void) 
{ 
    
       (y, x) = self.scr.getyx()                            
       curses.noecho() 
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1) 
       # Just added leaveok. 
       self.scr.leaveok(0)                      
       self.scr.setscrreg(0, 22) 
       self.stuff = ""          
       
       # Set the default column width. 
       self.colwidth = 7          
       # Move to the origin.        
       self.scr.move(1, 7)                       
       # Create a cell
       self.cell = cell(self.scr)                                            
       # Write the row and column headings.                             
       self.colheads = list(chr(x) for x in range(65,75)) 
       self.plist = list( (y,x) for y in range(1, 2) for 
          x in range(7, 75, 7) )
       self.cell.write_range(self.colheads, self.plist, 
            curses.A_STANDOUT, "center")  
       self.scr.refresh() 	
       # Row headings 
       self.scr.move(2, 0)         
       self.rowheads = list(range(1,21))  
       self.plist = list( (y,x) for y in range(2, 22) for 
          x in range(0, 1) )
       self.cell.write_range(self.rowheads, self.plist, 
            curses.A_STANDOUT, "center")  
       self.scr.refresh() 	
       # The position (2, 7) puts the cell perfectly in position 
       # at cell "A1".                          
       self.scr.move(2, 7)
       self.cell = cell(self.scr)                                      
       self.scr.refresh()  
       
       self.cell.move("R")
       (y, x) = self.scr.getyx()                            
       self.cell.write("123") 
       self.align() 
       self.scr.refresh()  
       
       self.cell.move("D")
       (y, x) = self.scr.getyx()                            
       self.cell.write("abc") 
       self.align() 
       self.scr.refresh()  
       
       self.cell.move("D")
       (y, x) = self.scr.getyx()                            
       self.cell.write("456") 
       self.align() 
       self.scr.refresh()  
                
       self.cell.move("D")
       self.scr.addstr(y, x, str(self.value) )                
       self.scr.refresh()  
              
       self.cell.move("D")
       self.scr.addstr(y, x, str(self.value) )                       
       self.scr.refresh()  
                                          
       self.cell.move("D")
       self.scr.refresh()    
                      
    
}     
    





/* Move to the beginning of the next line */ 
void nextline() 
{ 
   move(r+1, 0); 
   getyx(mywin, r, c);
   refresh();     
}     

void delchar() 
{    
   delch();   
   refresh();             
}     


void up()
{
  getyx(mywin, r, c);
  move(r-1, c);     
  refresh();                  
} 


void down()
{
  getyx(mywin, r, c);
  move(r+1, c);     
  refresh();                  
} 


void right()
{
  getyx(mywin, r, c);
  move(r, c+1);     
  refresh();                      
} 


void left() 
{
  getyx(mywin, r, c);
  move(r, c-1);     
  refresh();            
} 


void backspace()
{   
  getyx(mywin, r, c);
  move(r, c-1);   
  delch();   
  refresh();       
}     
    
int insert() 
{    
   if (insmode == 0) insmode = 1; 
   else if (insmode == 1) insmode = 0;        
   return insmode; 
}     


void put(int ch)
{   
   getyx(mywin, r, c); 
   if (insmode == 0) addch(ch);    
   else if (insmode == 1) insch(ch); 
   refresh();     
}     


void test() 
{ 
   getyx(mywin, r, c); 
   addstr("Just a small test string..."); 
   refresh(); 
}     




/*  Handle the keyboard input  */ 
void keyhandler() 
{ 
  
  getyx(mywin, r, c);
  /*  Handle input here */    
  ch = getch();   
  if (ch == KEY_BACKSPACE)    backspace();  
  else if (ch == KEY_DC)      delch(); 
  else if (ch == KEY_LEFT)    left(); 
  else if (ch == KEY_RIGHT)   right(); 
  else if (ch == KEY_UP)      up();
  else if (ch == KEY_DOWN)    down();     
  else if (ch == KEY_IC)      insert();      
  else put(ch); 
                        
}     




int main(int argc, char *argv[])
{    
         
   /* Initialise the screen  */    
   mywin = initscr();
   noecho();
   raw();  
   keypad(stdscr, TRUE);       
   scrollok(mywin,1);    
   idcok(mywin, 1); 
   idlok(mywin, 1);   
   /*  Get the size of the window  */ 
   getmaxyx(mywin, nrows, ncols); 
   clear(); 
   refresh(); 
   
   /*  Set row and col */ 
   r=0; c=0; 
      
   /*  The main loop  */  
   while(1) 
   {  
          
     keyhandler(); 
                
   } 
                   
   echo(); 
   keypad(mywin, 0); 
   endwin();
   
   return 0; 
                  
}




