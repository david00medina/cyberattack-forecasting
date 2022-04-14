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
CREATE TABLE `user_stats_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `lang` VARCHAR(2) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;