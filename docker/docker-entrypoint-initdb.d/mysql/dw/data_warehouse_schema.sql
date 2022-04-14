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



DROP TABLE IF EXISTS `label_dimension`;
CREATE TABLE `label_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `label` INTEGER UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `tweet_stats_dimension`;
CREATE TABLE `tweet_stats_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `quote_count` INTEGER UNSIGNED NULL,
  `reply_count` INTEGER UNSIGNED NULL,
  `retweet_count` INTEGER UNSIGNED NULL,
  `favorite_count` INTEGER UNSIGNED NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `country_dimension`;
CREATE TABLE `country_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `alpha2_code` CHAR(2) NOT NULL,
  `alpha3_code` CHAR(3) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `point_dimension`;
CREATE TABLE `point_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `latitude` FLOAT NOT NULL UNIQUE,
  `longitude` FLOAT NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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


DROP TABLE IF EXISTS `user_stats_dimension`;
CREATE TABLE `user_stats_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `followers_count` INTEGER UNSIGNED NULL,
  `friends_count` INTEGER UNSIGNED NULL,
  `listed_count` INTEGER UNSIGNED NULL,
  `favorites_count` INTEGER UNSIGNED NULL,
  `statuses_count` INTEGER UNSIGNED NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `lang_dimension`;
CREATE TABLE `lang_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `lang` VARCHAR(2) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `user_dimension`;
CREATE TABLE `user_dimension` (
  `id` BIGINT UNSIGNED NOT NULL,
  `place_id` BIGINT UNSIGNED NULL,
  `user_stats_id` BIGINT UNSIGNED NULL,
  `lang_id` BIGINT UNSIGNED NULL,
  `created_at_id` BIGINT UNSIGNED NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `screen_name` VARCHAR(265) NOT NULL UNIQUE,
  `description` LONGTEXT NULL,
  `default_profile` TINYINT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`place_id`) REFERENCES `place_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`user_stats_id`) REFERENCES `user_stats_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`lang_id`) REFERENCES `lang_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`created_at_id`) REFERENCES `datetime_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `tweet_fact`;
CREATE TABLE `tweet_fact` (
  `id` BIGINT UNSIGNED NOT NULL,
  `created_at_id` BIGINT UNSIGNED NOT NULL,
  `label_id` BIGINT UNSIGNED NOT NULL,
  `tweet_stats_id` BIGINT UNSIGNED NULL,
  `user_id` BIGINT UNSIGNED NULL,
  `coordinates_id` BIGINT UNSIGNED NULL,
  `bounding_box_id` BIGINT UNSIGNED NULL,
  `place_id` BIGINT UNSIGNED NULL,
  `in_tweet_reply_id` BIGINT UNSIGNED NULL,
  `in_reply_to_user_id` BIGINT UNSIGNED NULL,
  `quoted_status_id` BIGINT UNSIGNED NULL,
  `text` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`, `created_at_id`, `label_id`),
  FOREIGN KEY (`created_at_id`) REFERENCES `datetime_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`label_id`) REFERENCES `label_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`tweet_stats_id`) REFERENCES `tweet_stats_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`user_id`) REFERENCES `user_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`coordinates_id`) REFERENCES `coordinates_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`bounding_box_id`) REFERENCES `bounding_box_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`place_id`) REFERENCES `place_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`in_tweet_reply_id`) REFERENCES `tweet_fact` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`in_reply_to_user_id`) REFERENCES `user_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
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
