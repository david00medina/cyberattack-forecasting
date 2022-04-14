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

DROP TABLE IF EXISTS `tweet_fact`;
CREATE TABLE `tweet_fact` (
  `id` BIGINT UNSIGNED NOT NULL,
  `created_at_id` BIGINT UNSIGNED NOT NULL,
  `label_id` BIGINT UNSIGNED NOT NULL,
  `tweet_stats_id` BIGINT UNSIGNED NOT NULL,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `coordinates_id` BIGINT UNSIGNED NULL,
  `bounding_box_id` BIGINT UNSIGNED NULL,
  `place_id` BIGINT UNSIGNED NULL,
  `tweet_reply_id` BIGINT UNSIGNED NULL,
  `quoted_status_id` BIGINT UNSIGNED NULL,
  `text` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`, `created_at_id`, `label_id`, `tweet_stats_id`, `user_id`),
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
  FOREIGN KEY (`tweet_reply_id`) REFERENCES `tweet_reply_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`quoted_status_id`) REFERENCES `tweet_quoted_status_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
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


DROP TABLE IF EXISTS `tweet_quoted_status_dimension`;
CREATE TABLE `tweet_quoted_status_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `quoted_status_id` INTEGER UNSIGNED NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`quoted_status_id`) REFERENCES `tweet_fact` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `tweet_reply_dimension`;
CREATE TABLE `tweet_reply_dimension` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `in_reply_to_status_id` BIGINT UNSIGNED NOT NULL,
  `in_reply_to_user_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`in_reply_to_status_id`) REFERENCES `tweet_fact` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT,
  FOREIGN KEY (`in_reply_to_user_id`) REFERENCES `user_dimension` (`id`)
                          ON DELETE RESTRICT
                          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;