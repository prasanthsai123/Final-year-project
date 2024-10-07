/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - face_biometric
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`face_biometric` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `face_biometric`;

/*Table structure for table `exam_paper` */

DROP TABLE IF EXISTS `exam_paper`;

CREATE TABLE `exam_paper` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `a` varchar(100) DEFAULT NULL,
  `b` text,
  `c` text,
  `d` text,
  `e` text,
  `f` text,
  `g` text,
  `hh` text,
  `i` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `exam_paper` */

insert  into `exam_paper`(`id`,`a`,`b`,`c`,`d`,`e`,`f`,`g`,`hh`,`i`) values (1,'1','What is a correct syntax to output \"Hello World\" in Java?','print(\"Hello World\")','System.out.println(\"Hello World\")','echo(\"Hello World\")','Hello World','B','Basic Python  ','2022-04-19'),(2,'4','What is the correct file extension for Python files?','.pt','.java','.py','.html','C','Basic Python  ','2022-04-19'),(3,'2','How do you insert COMMENTS in Python code?','//','#','/*','*','B','Basic Python  ','2022-04-19');

/*Table structure for table `finalresults` */

DROP TABLE IF EXISTS `finalresults`;

CREATE TABLE `finalresults` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` text,
  `semail` text,
  `ename` text,
  `edate` text,
  `ca` text,
  `ua` text,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `finalresults` */

insert  into `finalresults`(`id`,`sid`,`semail`,`ename`,`edate`,`ca`,`ua`,`status`) values (1,'4560','cse.takeoff@gmail.com','Basic Python  ','2022-04-16','4','4',NULL),(2,'4560','cse.takeoff@gmail.com','Basic Python  ','2022-04-19','1','3',NULL);

/*Table structure for table `qsn_ans` */

DROP TABLE IF EXISTS `qsn_ans`;

CREATE TABLE `qsn_ans` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `qsn` varchar(100) DEFAULT NULL,
  `opt1` varchar(100) DEFAULT NULL,
  `opt2` varchar(100) DEFAULT NULL,
  `opt3` varchar(100) DEFAULT NULL,
  `opt4` varchar(100) DEFAULT NULL,
  `ans` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `qsn_ans` */

insert  into `qsn_ans`(`id`,`qsn`,`opt1`,`opt2`,`opt3`,`opt4`,`ans`) values (1,'What is a correct syntax to output \"Hello World\" in Java?','print(\"Hello World\")','System.out.println(\"Hello World\")','echo(\"Hello World\")','Hello World','B'),(2,'How do you insert COMMENTS in Python code?','//','#','/*','*','B'),(3,'Which one is NOT a legal variable name?','my_var','my-var','_myval','Myval','B'),(4,'What is the correct file extension for Python files?','.pt','.java','.py','.html','C');

/*Table structure for table `results` */

DROP TABLE IF EXISTS `results`;

CREATE TABLE `results` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` text,
  `sname` text,
  `semail` text,
  `ename` text,
  `edate` text,
  `ca` text,
  `ua` text,
  `status` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `results` */

insert  into `results`(`id`,`sid`,`sname`,`semail`,`ename`,`edate`,`ca`,`ua`,`status`) values (1,'4560','lakshmi','cse.takeoff@gmail.com','Basic Python  ','2022-04-19','B','A','Fake'),(2,'4560','lakshmi','cse.takeoff@gmail.com','Basic Python  ','2022-04-19','C','B','Fake'),(3,'4560','lakshmi','cse.takeoff@gmail.com','Basic Python  ','2022-04-19','B','B','Fake');

/*Table structure for table `user_registration` */

DROP TABLE IF EXISTS `user_registration`;

CREATE TABLE `user_registration` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` int(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `uname` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `d1` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `user_registration` */

insert  into `user_registration`(`id`,`sid`,`name`,`email`,`uname`,`pwd`,`pno`,`addr`,`d1`) values (1,4560,'lakshmi','cse.takeoff@gmail.com','lakshmi','123','9010867746','tirupati',NULL),(2,2990,'divya','reshmaashok2000@gmail.com','divya','123','7894561230','fgh','2022-04-14');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
