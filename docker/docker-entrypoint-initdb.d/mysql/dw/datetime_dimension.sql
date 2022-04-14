/************************************************************************************************************
 * Copyright (c) 2022 David Alberto Medina Medina.                                                          *
 *                                                                                                          *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software            *
 * and associated documentation files (the "Software"), to deal in the Software without restriction,        *
 *  including without limitation the rights to use, copy, modify, merge, publish, distribute,               *
 *   sublicense, and/or sell copies of the Software, and to permit persons to whom the Software             *
 *   is furnished to do so, subject to the following conditions:                                            *
 *                                                                                                          *
 * The above copyright notice and this permission notice shall be included in all copies or substantial     *
 * portions of the Software.                                                                                *
 *                                                                                                          *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,                      *
 *  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A                           *
 *  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR                                *
 *  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN                       *
 *  AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION                         *
 *  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                         *
 ************************************************************************************************************/

DROP TABLE IF EXISTS `datetime_dimension`;
CREATE TABLE `datetime_dimension` (
  `id` BIGINT UNSIGNED NOT NULL,
  `date_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `time_id` BIGINT UNSIGNED NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`date_id`) REFERENCES `date_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`time_id`) REFERENCES `time_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `date_dimension`;
CREATE TABLE `date_dimension` (
  `id` BIGINT UNSIGNED NOT NULL,
  `year_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `month_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `day_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`year_id`) REFERENCES `year_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`month_id`) REFERENCES `month_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`day_id`) REFERENCES `day_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




DROP TABLE IF EXISTS `time_dimension`;
CREATE TABLE `time_dimension` (
  `id` BIGINT UNSIGNED NOT NULL,
  `hour_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `minute_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `second_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`hour_id`) REFERENCES `hour_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`minute_id`) REFERENCES `minute_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`second_id`) REFERENCES `second_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `year_dimension`;
CREATE TABLE `year_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `year` TINYINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `month_dimension`;
CREATE TABLE `month_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `month` TINYINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `day_dimension`;
CREATE TABLE `day_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `day` TINYINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `hour_dimension`;
CREATE TABLE `hour_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `hour` TINYINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `minute_dimension`;
CREATE TABLE `minute_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `minute` TINYINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `second_dimension`;
CREATE TABLE `second_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `second` FLOAT(11, 9) UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;