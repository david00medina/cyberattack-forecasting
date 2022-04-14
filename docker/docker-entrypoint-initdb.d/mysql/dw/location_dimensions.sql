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

DROP TABLE IF EXISTS `bounding_box_dimension`;
CREATE TABLE `bounding_box_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `lower_left_point_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `upper_left_point_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `upper_right_point_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  `lower_right_point_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`lower_left_point_id`) REFERENCES `point_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`upper_left_point_id`) REFERENCES `point_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`upper_right_point_id`) REFERENCES `point_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`lower_right_point_id`) REFERENCES `point_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `coordinates_dimension`;
CREATE TABLE `coordinates_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `point_id` BIGINT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`point_id`) REFERENCES `point_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `point_dimension`;
CREATE TABLE `point_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `latitude` FLOAT NOT NULL UNIQUE,
  `longitude` FLOAT NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `place_dimension`;
CREATE TABLE `place_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `country_id` BIGINT UNSIGNED NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `full_name` VARCHAR(256) NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`country_id`) REFERENCES `country_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `country_dimension`;
CREATE TABLE `country_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `alpha2_code` CHAR(2) NOT NULL,
  `alpha3_code` CHAR(3) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `withheld_dimension`;
CREATE TABLE `withheld_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tweet_id` BIGINT UNSIGNED NOT NULL,
  `country_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`tweet_id`) REFERENCES `tweet_fact` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`country_id`) REFERENCES `country_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;