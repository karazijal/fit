//
//  minHeader.h
//  LibraryFaultInjection
//
//  Created by Laurynas Karazija on 18/02/2016.
//  Copyright © 2016 Laurynas Karazija. All rights reserved.
//

#ifndef minHeader_h
#define minHeader_h


#include <stdio.h>
#include <sys/stat.h>
#include <sys/socket.h>

#ifdef __APPLE__
#define __ssize_t ssize_t
#define fpos64_t fpos_t
#define off64_t off_t
#endif


#include "Logfile.hpp"

#endif /* minHeader_h */

