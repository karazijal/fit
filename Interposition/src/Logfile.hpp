//
//  Logfile.hpp
//  LibraryFaultInjection
//
//  Created by Laurynas Karazija on 01/01/2016.
//  Copyright © 2016 Laurynas Karazija. All rights reserved.
//

#ifndef Logfile_hpp
#define Logfile_hpp


//needed for string and stdio.h definitions
//#include <stdio.h>  
//#include <string>




namespace FIT{
    class Logfile {
        FILE* lfile;
        int lfd;
        FILE* ofile;
        int ofd;
        FILE* efile;
        int efd;
        FILE* ifile;
        int ifd;
        FILE* pfile;
        int pfd;
        //FILE* internal_LOG;
//        std::string logfilenameout;
//        std::string logfilenamelog;
//        std::string logfilenameerr;
//        std::string logfilenameinp;
        bool shortlog_flag;
        bool logging_flag;
        bool input_logging_flag;
        
        //Will effectivelly make any I/O happen linearly;
        
        void writeTolog(const void* str, const size_t size, const size_t nmemb, FILE* file);
        
        
        
        FILE* directFD(int fd);
        
        void logChar(FILE* fp,const int c);
        void logString(FILE* fp, const char * s,const  size_t size);
        void logComplex(FILE* fp, const void * ptr, const size_t size, const size_t nmemb);
//        void logComplexByte(FILE* fp, void * buf, size_t count);
        void logWs(FILE* fp, const wchar_t * ws, const size_t size);
//        void logFormat(FILE* fp, char * format, va_list ap);
//        void logFormatWs(FILE* fp,  wchar_t * format, va_list ap);
        
        //logFailure Function -> will abort everything!!!
        void logFailure(const char*);
        
    public:
        Logfile(const bool sl,const bool lf,const  bool ilf,const  char* lfo, const char* lfl, const char* lfe,const  char* lfi, const char* lfp);
        ~Logfile();

        bool isProtected(const int fd);
        void isExempt(const char * filename);
        
        void log_call(const char * function);
        void log_call(const char * function, size_t nb);
        
        void log_input_c(const int c);
        void log_output_c(const int fd, const int c);
        
        void log_input_str(const char * s, const int size);
        void log_output_str(const int fd,const char * s,const size_t size);
        
        void log_input_clx(const void * ptr, const size_t size, const size_t nmemb);
        void log_output_clx(const int fd, const void * ptr, const size_t size, const size_t nmemb);
        
//        void log_input_ws(wchar_t * ws, size_t size);
//        void log_output_ws(int fd, wchar_t * ws, size_t size);
        
        
        
    };
}
#endif /* Logfile_hpp */