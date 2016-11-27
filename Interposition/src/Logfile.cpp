//
//  Logfile.cpp
//  LibraryFaultInjection
//
//  Created by Laurynas Karazija on 01/01/2016.
//  Copyright © 2016 Laurynas Karazija. All rights reserved.
//


#include <stdlib.h>
#include <string.h>
//#include <time.h>
#include <mutex>
#include "Orig.hpp"
#include "Logfile.hpp"


using namespace std;
using namespace FIT;

static mutex mux;



//Logfile::Logfile(bool sl, bool lf, bool ilf, string lfo, string lfl, string lfe, string lfi) : shortlog_flag(sl),logging_flag(lf), input_logging_flag(ilf), logfilenameout(lfo), logfilenamelog(lfl),logfilenameerr(lfe),logfilenameinp(lfi){
//    if(logging_flag){
//        if(!shortlog_flag){
//            lfile = fopen(logfilenamelog.c_str(), "w"); //!
//            if (lfile == NULL){
//                this->logFailure("Could not create logfile");
//            }
//            lfd = fileno(lfile);
//            ofile = fopen(logfilenameout.c_str(), "w");
//            if (ofile == NULL){
//                this->logFailure("Could not create stdout logfile");
//            }
//            ofd = fileno(ofile);
//            efile = fopen(logfilenameerr.c_str(), "w"); //!
//            if (efile == NULL){
//                this->logFailure("Could not create error logfile");
//            }
//            
//            if (input_logging_flag){
//                ifile = fopen(logfilenameinp.c_str(), "w"); //!
//                if (ifile == NULL){
//                    this->logFailure("Could not create input logfile");
//                }
//            }
//        } else {
//            lfile = stdout;
//            ofile = stdout;
//            efile = stderr;
//            if (input_logging_flag){
//                ifile = fopen(logfilenameinp.c_str(), "w"); //!
//                if (ifile == NULL){
//                    this->logFailure("Could not create input logfile");
//                }
//            } else {
//                ifile = stdout;
//            }
//        }
//        lfd = fileno(lfile);
//        ofd = fileno(ofile);
//        efd = fileno(efile);
//        ifd = fileno(ifile);
//    }
//}
Logfile::Logfile(const bool sl, const bool lf,const  bool ilf, const char* lfo, const char* lfl, const char* lfe, const char* lfi, const char* lfp) : shortlog_flag(sl),logging_flag(lf), input_logging_flag(ilf){
    lfd = -1; lfile = NULL;
    ofd = -1; ofile = NULL;
    efd = -1; efile = NULL;
    ifd = -1; ifile = NULL;
    pfd = -1; pfile = NULL;
    if(logging_flag){
        pfile = Original.fopen_(lfp, "w");
        if (pfile == NULL){
            Original.fputs_("@E: Logging init error\n", stdout);
            abort();
        }
        if(!shortlog_flag){
            lfile = Original.fopen_(lfl, "w"); //!
            if (lfile == NULL){
                this->logFailure("@E: Could not create logfile");
            }
            lfd = fileno(lfile);
            ofile = Original.fopen_(lfo, "w");
            if (ofile == NULL){
                this->logFailure("@E: Could not create stdout logfile");
            }
            ofd = fileno(ofile);
            efile = Original.fopen_(lfe, "w"); //!
            if (efile == NULL){
                this->logFailure("@E: Could not create error logfile");
            }
            
            if (input_logging_flag){
                ifile = Original.fopen_(lfi, "w"); //!
                if (ifile == NULL){
                    this->logFailure("@E: Could not create input logfile");
                }
            }
        } else {
            lfile = stdout;
            ofile = stdout;
            efile = stderr;
            if (input_logging_flag){
                ifile = Original.fopen_(lfi, "w"); //!
                if (ifile == NULL){
                    this->logFailure("@E: Could not create input logfile");
                }
            } else {
                ifile = stdout;
            }
        }
        lfd = fileno(lfile);
        ofd = fileno(ofile);
        efd = fileno(efile);
        ifd = fileno(ifile);
        pfd = fileno(pfile);
        log_call("Session Start\n");
    }
}


Logfile::~Logfile(){
    if (logging_flag){
        //Flush files...
        fflush(lfile);
        fflush(ofile);
        fflush(efile);
        fflush(pfile);
        if (input_logging_flag){
            fflush(ifile);
        }
        if (input_logging_flag){
            if (Original.fclose_(ifile) == EOF)
                this->logFailure("@E: Log Close Failure, Log files may be incomplete");
        }
        if(!shortlog_flag){
            if (Original.fclose_(lfile) == EOF)
                this->logFailure("@E: Log Close Failure, Log files may be incomplete");
            if (Original.fclose_(ofile) == EOF)
                this->logFailure("@E: Log Close Failure, Log files may be incomplete");
            if (Original.fclose_(efile) == EOF)
                this->logFailure("@E: Log Close Failure, Log files may be incomplete");
        }
        if (Original.fclose_(pfile) == EOF)
            abort();
    }
}

void Logfile::logFailure(const char* msg){
    //TODO:: change to printf
    log_call(msg);
    abort();
}

//void Logfile::logout(const char* str){
//    return this->logout(str, strlen(str));
//}
//void Logfile::logout(string s){
//    return this->logout(s.c_str(), s.length()+1);
//}
//void Logfile::logout(const char* str, size_t size){
//    return this->writeTolog(str, size, ofile);
//}
//
//
//void Logfile::logerr(const char* str){
//    return this->logerr(str, strlen(str));
//}
//void Logfile::logerr(string s){
//    return this->logerr(s.c_str(), s.length()+1);
//}
//void Logfile::logerr(const char* str, size_t size){
//    return this->writeTolog(str, size, efile);
//}
//
//
//void Logfile::loginp(const char* str){
//    return this->loginp(str, strlen(str));
//}
//void Logfile::loginp(string s){
//    return this->loginp(s.c_str(), s.length()+1);
//}
//void Logfile::loginp(const char* str, size_t size){
//    if (input_logging_flag) {
//        return this->writeTolog(str, size, ifile);
//    }
//}
//
//void Logfile::log(const char* str){
//    return this->log(str, strlen(str));
//}
//void Logfile::log(string s){
//    return this->log(s.c_str(), s.length()+1);
//}
//void Logfile::log(const char* str, size_t size){
//    return this->writeTolog(str, size, lfile);
//}

FILE* Logfile::directFD(const int fd){
    if (fd==fileno(stdout)){
        return ofile;
    } else if (fd==fileno(stderr)){
        return efile;
    }
    return lfile;
}
void Logfile::logChar(FILE* fp, const int c){
    char aux = (char) c;
    char* p_aux = &aux;
    writeTolog(p_aux, sizeof(char), 1, fp);
}
void Logfile::logString(FILE* fp,const  char * s, const size_t size){
    writeTolog(s,sizeof(char), size,  fp);
}
void Logfile::logComplex(FILE* fp,const  void * ptr, const size_t size, const size_t nmemb){
    writeTolog(ptr, size, nmemb, fp);
}
void Logfile::logWs(FILE* fp, const wchar_t * ws,const  size_t size){
    writeTolog((void*) ws, sizeof(wchar_t), size, fp);
}
void Logfile::writeTolog(const void* str, const size_t size,const size_t nmemb, FILE* file){
    if (logging_flag) {
        size_t towrite = nmemb;
        size_t no_more = nmemb*2;
        const char* st = (char *)str;
        mux.lock();
        do{
            size_t written = Original.fwrite_(st, size, towrite, file);
            no_more--;
            if (no_more == 0){
                mux.unlock();
                this->logFailure("Could not write log/n");
                return;
            }
            towrite -= written;
            st += written* (size/sizeof(char));
        } while (towrite > 0);
#ifdef __APPLE__
        fflush(file);
#endif
        mux.unlock();
        return;
    }
}

bool Logfile::isProtected(const int fd){
    return fd==lfd && fd==ofd && fd==efd && fd==ifd && fd==pfd;
}

void Logfile::log_input_c(const int c){
    if (input_logging_flag){
        logChar(ifile, c);
    }
}
void Logfile::log_output_c(const int fd, const int c){
    logChar(directFD(fd), c);
}
void Logfile::log_input_str(const char * s,const  int size){
    if (input_logging_flag){
        logString(ifile, s, size);
    }
}
void Logfile::log_output_str(const int fd, const char * s, const size_t size){
    logString(directFD(fd), s, size);
}

void Logfile::log_input_clx(const void * ptr,const  size_t size,const  size_t nmemb){
    if (input_logging_flag){
        logComplex(ifile, ptr, size, nmemb);
    }
}
void Logfile::log_output_clx(const int fd,const  void * ptr, const size_t size, const size_t nmemb){
    logComplex(directFD(fd), ptr, size, nmemb);
}

void Logfile::log_call(const char * function){
    size_t len = stringlen(function);
    writeTolog(function,sizeof(char), len,  pfile);
}

void Logfile::log_call(const char * fun, size_t nb){
    writeTolog(fun, sizeof(char), nb, pfile);
}



