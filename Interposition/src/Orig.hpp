//
//  Orig.hpp
//  LibraryFaultInjection
//
//  Created by Laurynas Karazija on 01/01/2016.
//  Copyright (C)  2016 Laurynas Karazija. All rights reserved.
//
//
//  This file is automatically generated
//
#ifndef Orig_hpp
#define Orig_hpp

#include "minHeader.h"

namespace FIT{
    //initialised_flag
    //bool initialised_flag = false;
    extern struct Orig{
        bool injection_flag;
        bool debugmode_flag;
        bool recovery_flag;
        bool memory_flag;

        int (*vfprintf_)(FILE * stream, const char * format, va_list ap);
        int vfprintf_flag;
        int (*vdprintf_)(int fd, const char * format, va_list ap);
        int vdprintf_flag;
        int (*fgetc_unlocked_)(FILE * stream);
        int fgetc_unlocked_flag;
        int (*fputc_unlocked_)(int c, FILE * stream);
        int fputc_unlocked_flag;
        int (*__vfprintf_chk_)(FILE * stream, int flag, const char * format, va_list ap);
        int __vfprintf_chk_flag;
        int (*close_)(int fd);
        int close_flag;
        int (*creat_)(const char * pathname, mode_t mode);
        int creat_flag;
        int (*creat64_)(const char * pathname, mode_t mode);
        int creat64_flag;
        int (*fclose_)(FILE * fp);
        int fclose_flag;
        int (*fcloseall_)();
        int fcloseall_flag;
        int (*fgetc_)(FILE * stream);
        int fgetc_flag;
        char * (*fgets_)(char * s, int size, FILE * stream);
        int fgets_flag;
        FILE * (*fopen_)(const char * path, const char * mode);
        int fopen_flag;
        FILE * (*fopen64_)(const char * path, const char * mode);
        int fopen64_flag;
        int (*fputc_)(int c, FILE * stream);
        int fputc_flag;
        int (*fputs_)(const char * s, FILE * stream);
        int fputs_flag;
        size_t (*fread_)(void * ptr, size_t size, size_t nb, FILE * stream);
        int fread_flag;
        FILE * (*freopen_)(const char * path, const char * mode, FILE * stream);
        int freopen_flag;
        FILE * (*freopen64_)(const char * filename, const char * type, FILE * stream);
        int freopen64_flag;
        size_t (*fwrite_)(const void * ptr, size_t size, size_t nb, FILE * stream);
        int fwrite_flag;
        __ssize_t (*getline_)(char ** lineptr, size_t * n, FILE * stream);
        int getline_flag;
        ssize_t (*pread_)(int fd, void * ptr, size_t nb, off_t offset);
        int pread_flag;
        ssize_t (*pwrite_)(int fd, const void * ptr, size_t nb, off_t offset);
        int pwrite_flag;
        ssize_t (*read_)(int fd, void * ptr, size_t nb);
        int read_flag;
        int (*vfscanf_)(FILE * stream, const char * format, va_list ap);
        int vfscanf_flag;
        ssize_t (*write_)(int fd, const void * ptr, size_t nb);
        int write_flag;
        size_t (*fread_unlocked_)(void * ptr, size_t size, size_t nb, FILE * stream);
        int fread_unlocked_flag;
        size_t (*fwrite_unlocked_)(const void * ptr, size_t size, size_t nb, FILE * stream);
        int fwrite_unlocked_flag;
        char * (*fgets_unlocked_)(char * s, int n, FILE * stream);
        int fgets_unlocked_flag;
        int (*fputs_unlocked_)(const char * s, FILE * stream);
        int fputs_unlocked_flag;
        int (*fseek_)(FILE * stream, long offset, int whence);
        int fseek_flag;
        int (*fseeko_)(FILE * stream, off_t offset, int whence);
        int fseeko_flag;
        int (*fsetpos_)(FILE * stream, const fpos_t * pos);
        int fsetpos_flag;
        int (*fsetpos64_)(FILE * stream, const fpos64_t * pos);
        int fsetpos64_flag;
        off_t (*lseek_)(int fd, off_t offset, int whence);
        int lseek_flag;
        off64_t (*lseek64_)(int fd, off64_t offset, int whence);
        int lseek64_flag;
        int (*chmod_)(const char * path, mode_t mode);
        int chmod_flag;
        int (*chown_)(const char * path, uid_t owner, gid_t group);
        int chown_flag;
        int (*fchmod_)(int fd, mode_t mode);
        int fchmod_flag;
        int (*fchown_)(int fd, uid_t owner, gid_t group);
        int fchown_flag;
        int (*lchown_)(const char * path, uid_t owner, gid_t group);
        int lchown_flag;
        int (*dup_)(int oldfd);
        int dup_flag;
        int (*dup2_)(int oldfd, int newfd);
        int dup2_flag;
        int (*dup3_)(int oldfd, int newfd, int flags);
        int dup3_flag;
        int (*ftruncate_)(int fd, off_t length);
        int ftruncate_flag;
        int (*ftruncate64_)(int fd, off64_t length);
        int ftruncate64_flag;
        int (*link_)(const char * path1, const char * path2);
        int link_flag;
        int (*mkdir_)(const char * pathname, mode_t mode);
        int mkdir_flag;
        int (*mkfifo_)(const char * pathname, mode_t mode);
        int mkfifo_flag;
        int (*__xmknod_)(int __ver, const char * pathname, mode_t mode, dev_t* dev);
        int __xmknod_flag;
        int (*remove_)(const char * pathname);
        int remove_flag;
        int (*rename_)(const char * oldpath, const char * newpath);
        int rename_flag;
        int (*rmdir_)(const char * pathname);
        int rmdir_flag;
        int (*symlink_)(const char * oldpath, const char * newpath);
        int symlink_flag;
        int (*truncate_)(const char * path, off_t length);
        int truncate_flag;
        int (*truncate64_)(const char * path, off64_t length);
        int truncate64_flag;
        int (*unlink_)(const char * pathname);
        int unlink_flag;
        FILE * (*popen_)(const char * command, const char * type);
        int popen_flag;
        int (*pclose_)(FILE * stream);
        int pclose_flag;
        int (*mkstemp_)(char * templ);
        int mkstemp_flag;
        int (*mkostemp_)(char * templ, int flags);
        int mkostemp_flag;
        int (*mkstemps_)(char * templ, int suffixlen);
        int mkstemps_flag;
        int (*mkostemps_)(char * templ, int suffixlen, int flags);
        int mkostemps_flag;
        FILE * (*tmpfile_)();
        int tmpfile_flag;
        FILE * (*tmpfile64_)();
        int tmpfile64_flag;
        int (*__fxstat_)(int __ver, int fd, struct stat * buf);
        int __fxstat_flag;
        int (*__fxstat64_)(int __ver, int fd, struct stat64 * buf);
        int __fxstat64_flag;
        int (*__lxstat_)(int __ver, const char * path, struct stat * buf);
        int __lxstat_flag;
        int (*__lxstat64_)(int __ver, const char * path, struct stat64 * buf);
        int __lxstat64_flag;
        int (*__xstat_)(int __ver, const char * path, struct stat * buf);
        int __xstat_flag;
        int (*__xstat64_)(int __ver, const char * path, struct stat64 * buf);
        int __xstat64_flag;
        int (*chdir_)(const char * path);
        int chdir_flag;
        int (*fchdir_)(int fd);
        int fchdir_flag;
        int (*killpg_)(int pgrp, int sig);
        int killpg_flag;
        int (*seteuid_)(uid_t euid);
        int seteuid_flag;
        int (*setegid_)(gid_t egid);
        int setegid_flag;
        int (*setgid_)(gid_t gid);
        int setgid_flag;
        int (*setreuid_)(uid_t ruid, uid_t euid);
        int setreuid_flag;
        int (*setregid_)(gid_t rgid, gid_t egid);
        int setregid_flag;
        int (*setuid_)(uid_t uid);
        int setuid_flag;
        int (*clearenv_)();
        int clearenv_flag;
        int (*putenv_)(char * string);
        int putenv_flag;
        int (*setenv_)(const char * name, const char * value, int overwrite);
        int setenv_flag;
        int (*unsetenv_)(const char * name);
        int unsetenv_flag;
        int (*open_)(const char *pathname, int flags, ...);
        int open_flag;
        int (*open64_)(const char *pathname, int flags, ...);
        int open64_flag;
        int (*socket_)(int domain, int type, int protocol);
        int socket_flag;
        int (*accept_)(int sockfd, struct sockaddr * addr, socklen_t * addrlen);
        int accept_flag;
        int (*pipe_)(int * pipefd);
        int pipe_flag;
        int (*pipe2_)(int * pipefd, int flags);
        int pipe2_flag;
        char * (*__fgets_chk_)(char * s, size_t size, int strsize, FILE * stream);
        int __fgets_chk_flag;
        char * (*__fgets_unlocked_chk_)(char * s, size_t size, int strsize, FILE * stream);
        int __fgets_unlocked_chk_flag;
        wchar_t * (*__fgetws_chk_)(wchar_t * ws, size_t size, int strsize, FILE * stream);
        int __fgetws_chk_flag;
        wchar_t * (*__fgetws_unlocked_chk_)(wchar_t * ws, size_t strsize, int n, FILE * stream);
        int __fgetws_unlocked_chk_flag;
        ssize_t (*__pread64_chk_)(int fd, void * ptr, size_t nb, off64_t offset, size_t buflen);
        int __pread64_chk_flag;
        ssize_t (*__pread_chk_)(int fd, void * ptr, size_t nb, off_t offset, size_t buflen);
        int __pread_chk_flag;
        ssize_t (*__read_chk_)(int fd, void * ptr, size_t nb, size_t buflen);
        int __read_chk_flag;
        int (*openat_)(int dirfd, const char *pathname, int flags, ...);
        int openat_flag;
        int (*openat64_)(int dirfd, const char *pathname, int flags, ...);
        int openat64_flag;
        int (*renameat_)(int olddirfd, const char * oldpath, int newdirfd, const char * newpath);
        int renameat_flag;
        int (*mkfifoat_)(int dirfd, const char * pathname, mode_t mode);
        int mkfifoat_flag;
        int (*symlinkat_)(const char * oldpath, int newdirfd, const char * newpath);
        int symlinkat_flag;
        int (*mkdirat_)(int dirfd, const char * pathname, mode_t mode);
        int mkdirat_flag;
        int (*unlinkat_)(int dirfd, const char * pathname, int flags);
        int unlinkat_flag;
        int (*fchmodat_)(int dirfd, const char * pathname, mode_t mode, int flags);
        int fchmodat_flag;
        int (*fchownat_)(int dirfd, const char * pathname, uid_t owner, gid_t group, int flags);
        int fchownat_flag;
        int (*linkat_)(int olddirfd, const char * oldpath, int newdirfd, const char * newpath, int flags);
        int linkat_flag;
        
        int vfprintf_count;
        int vdprintf_count;
        int fgetc_unlocked_count;
        int fputc_unlocked_count;
        int __vfprintf_chk_count;
        int close_count;
        int creat_count;
        int creat64_count;
        int fclose_count;
        int fcloseall_count;
        int fgetc_count;
        int fgets_count;
        int fopen_count;
        int fopen64_count;
        int fputc_count;
        int fputs_count;
        int fread_count;
        int freopen_count;
        int freopen64_count;
        int fwrite_count;
        int getline_count;
        int pread_count;
        int pwrite_count;
        int read_count;
        int vfscanf_count;
        int write_count;
        int fread_unlocked_count;
        int fwrite_unlocked_count;
        int fgets_unlocked_count;
        int fputs_unlocked_count;
        int fseek_count;
        int fseeko_count;
        int fsetpos_count;
        int fsetpos64_count;
        int lseek_count;
        int lseek64_count;
        int chmod_count;
        int chown_count;
        int fchmod_count;
        int fchown_count;
        int lchown_count;
        int dup_count;
        int dup2_count;
        int dup3_count;
        int ftruncate_count;
        int ftruncate64_count;
        int link_count;
        int mkdir_count;
        int mkfifo_count;
        int __xmknod_count;
        int remove_count;
        int rename_count;
        int rmdir_count;
        int symlink_count;
        int truncate_count;
        int truncate64_count;
        int unlink_count;
        int popen_count;
        int pclose_count;
        int mkstemp_count;
        int mkostemp_count;
        int mkstemps_count;
        int mkostemps_count;
        int tmpfile_count;
        int tmpfile64_count;
        int __fxstat_count;
        int __fxstat64_count;
        int __lxstat_count;
        int __lxstat64_count;
        int __xstat_count;
        int __xstat64_count;
        int chdir_count;
        int fchdir_count;
        int killpg_count;
        int seteuid_count;
        int setegid_count;
        int setgid_count;
        int setreuid_count;
        int setregid_count;
        int setuid_count;
        int clearenv_count;
        int putenv_count;
        int setenv_count;
        int unsetenv_count;
        int open_count;
        int open64_count;
        int socket_count;
        int accept_count;
        int pipe_count;
        int pipe2_count;
        int __fgets_chk_count;
        int __fgets_unlocked_chk_count;
        int __fgetws_chk_count;
        int __fgetws_unlocked_chk_count;
        int __pread64_chk_count;
        int __pread_chk_count;
        int __read_chk_count;
        int openat_count;
        int openat64_count;
        int renameat_count;
        int mkfifoat_count;
        int symlinkat_count;
        int mkdirat_count;
        int unlinkat_count;
        int fchmodat_count;
        int fchownat_count;
        int linkat_count;
        

        Logfile* logFile;
    } Original;
    extern bool initialised_flag;
    extern bool insideFIT;
}
size_t stringlen(const char* ptr);
int rnd();
void __FIT__injectionInit();
void __FIT__injectionFin();



#endif /* Orig_hpp */