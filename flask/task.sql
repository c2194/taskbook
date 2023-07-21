-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2023-07-12 17:56:07
-- 服务器版本： 5.7.26
-- PHP 版本： 7.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `task`
--

-- --------------------------------------------------------

--
-- 表的结构 `departments`
--

CREATE TABLE `departments` (
  `department_id` int(11) NOT NULL,
  `department_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `manager_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `departments`
--

INSERT INTO `departments` (`department_id`, `department_name`, `manager_name`) VALUES
(4, '生产售后部', NULL),
(2, '直播运营部', NULL),
(3, '市场业务部', NULL),
(1, '技术开发部', NULL),
(5, '职能管理部', NULL),
(6, '门店运营部', NULL);

-- --------------------------------------------------------

--
-- 表的结构 `department_members`
--

CREATE TABLE `department_members` (
  `member_id` int(11) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `department_members`
--

INSERT INTO `department_members` (`member_id`, `department_id`, `user_id`) VALUES
(1, 3, 1),
(2, 3, 2),
(3, 3, 3),
(4, 3, 4),
(5, 3, 5),
(6, 3, 6),
(7, 3, 7),
(8, 3, 8),
(9, 3, 9),
(10, 3, 10),
(11, 2, 10),
(12, 2, 11),
(13, 4, 12),
(14, 4, 13),
(15, 4, 14),
(16, 4, 15),
(17, 4, 16),
(18, 4, 17),
(19, 4, 18),
(20, 4, 19),
(21, 4, 20),
(22, 4, 21),
(23, 4, 22),
(24, 4, 23),
(25, 1, 24),
(26, 1, 25),
(27, 1, 26),
(28, 1, 27),
(29, 1, 28),
(30, 1, 29),
(31, 1, 30),
(32, 5, 31),
(33, 5, 32),
(34, 5, 33),
(35, 5, 34),
(36, 5, 35),
(37, 6, 36),
(38, 6, 37),
(39, 6, 38),
(40, 6, 39),
(41, 6, 40),
(42, 6, 41),
(43, 6, 42),
(44, 6, 43),
(45, 6, 44),
(46, 6, 45),
(47, 6, 46),
(48, 6, 47);

-- --------------------------------------------------------

--
-- 表的结构 `department_user`
--

CREATE TABLE `department_user` (
  `department_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `discussions`
--

CREATE TABLE `discussions` (
  `id` int(11) NOT NULL COMMENT '讨论ID',
  `sub_task_id` int(11) DEFAULT NULL COMMENT '对应的子任务ID',
  `speaker_id` int(11) DEFAULT NULL COMMENT '发言者ID',
  `speak_time` datetime DEFAULT NULL COMMENT '发言时间',
  `work_tasks_id` int(11) NOT NULL COMMENT '主任务id',
  `type` int(2) NOT NULL COMMENT '是主任务还是子任务的',
  `text` text COLLATE utf8_unicode_ci NOT NULL COMMENT '留言内容'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='讨论表';

-- --------------------------------------------------------

--
-- 表的结构 `functions`
--

CREATE TABLE `functions` (
  `function_id` int(11) NOT NULL,
  `function_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `functions`
--

INSERT INTO `functions` (`function_id`, `function_name`) VALUES
(1, '新媒体运营'),
(2, '售后工程'),
(3, '工厂管理'),
(4, '工厂管理助理'),
(5, '仓管'),
(6, '售后管理'),
(7, '工厂工程'),
(8, '技术顾问'),
(9, '开发管理'),
(10, '开发'),
(11, '创意美术'),
(12, '全局运营管理'),
(13, '财资库债'),
(14, '财资库债管理'),
(15, '办公'),
(16, '人事'),
(17, '门店整体运管'),
(18, '门店运管协管'),
(19, '门店督导'),
(20, '门店培训'),
(21, '门店区域运管'),
(22, '门店运管'),
(23, '区域全局管理'),
(24, '区管助理'),
(25, '业务管理'),
(26, '业务管理助理'),
(27, '业务执管'),
(28, '业务带培');

-- --------------------------------------------------------

--
-- 表的结构 `function_members`
--

CREATE TABLE `function_members` (
  `member_id` int(11) NOT NULL,
  `function_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `function_members`
--

INSERT INTO `function_members` (`member_id`, `function_id`, `user_id`) VALUES
(1, 23, 1),
(2, 25, 2),
(3, 25, 3),
(4, 27, 4),
(5, 27, 5),
(6, 27, 6),
(7, 27, 7),
(8, 27, 8),
(9, 26, 8),
(10, 26, 9),
(11, 27, 9),
(12, 28, 9),
(13, 27, 10),
(14, 1, 11),
(15, 1, 12),
(16, 6, 13),
(17, 2, 14),
(18, 4, 15),
(19, 5, 16),
(20, 3, 17),
(21, 2, 18),
(22, 6, 18),
(23, 2, 19),
(24, 6, 19),
(25, 4, 20),
(26, 2, 21),
(27, 7, 22),
(28, 2, 23),
(29, 2, 24),
(30, 8, 25),
(31, 9, 26),
(32, 9, 27),
(33, 10, 27),
(34, 10, 28),
(35, 10, 29),
(36, 10, 30),
(37, 11, 31),
(38, 12, 32),
(39, 13, 33),
(40, 13, 34),
(41, 14, 34),
(42, 15, 35),
(43, 16, 35),
(44, 17, 36),
(45, 18, 36),
(46, 19, 37),
(47, 20, 38),
(48, 20, 39),
(49, 20, 40),
(50, 21, 41),
(51, 21, 42),
(52, 27, 43),
(53, 27, 44),
(54, 21, 45),
(55, 21, 46),
(56, 27, 47),
(57, 21, 48),
(58, 27, 49),
(59, 27, 50),
(60, 27, 51),
(61, 27, 52);

-- --------------------------------------------------------

--
-- 表的结构 `log`
--

CREATE TABLE `log` (
  `log_id` int(11) NOT NULL,
  `readme` text COLLATE utf8_unicode_ci NOT NULL COMMENT '说明',
  `user_id` int(11) NOT NULL COMMENT '操作者id',
  `ctrl` int(2) NOT NULL COMMENT '操作类型',
  `task_id` int(11) NOT NULL COMMENT '对应 work_tasks 表的 autoid',
  `sub_id` int(11) NOT NULL COMMENT '对应 sub_tasks 表的 id'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `setp_progress`
--

CREATE TABLE `setp_progress` (
  `sp_id` int(11) NOT NULL,
  `progress` int(2) NOT NULL COMMENT '完成进度',
  `sp_text` text COLLATE utf8_unicode_ci NOT NULL COMMENT '说明',
  `sp_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `step_id` int(11) NOT NULL COMMENT '对应step id'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `sub_tasks`
--

CREATE TABLE `sub_tasks` (
  `id` int(11) NOT NULL COMMENT '子任务ID',
  `task_id` int(11) DEFAULT NULL COMMENT '所属任务表的ID',
  `sub_task_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '子任务名称',
  `sub_task_description` text COLLATE utf8_unicode_ci COMMENT '子任务说明',
  `end_time` datetime DEFAULT NULL COMMENT '计划完成时间',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `create_user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `next_user_id` int(11) DEFAULT NULL COMMENT '下一步用户ID',
  `next_sub_task_id` int(11) DEFAULT NULL COMMENT '下一步子任务ID',
  `completion_rate` int(11) DEFAULT NULL COMMENT '完成度',
  `sub_user` int(11) NOT NULL COMMENT '子任务执行人',
  `state` int(2) NOT NULL COMMENT '状态',
  `sub_class` int(2) NOT NULL COMMENT '任务类型'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='子任务表';

-- --------------------------------------------------------

--
-- 表的结构 `sub_task_step`
--

CREATE TABLE `sub_task_step` (
  `id` int(11) NOT NULL,
  `completion_rate` int(11) NOT NULL COMMENT '完成率',
  `step_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '标题',
  `step_readme` text COLLATE utf8_unicode_ci NOT NULL COMMENT '说明',
  `sub_tasks_id` int(11) NOT NULL COMMENT '对应的子任务id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '顾名思义'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `task_execution`
--

CREATE TABLE `task_execution` (
  `id` int(11) NOT NULL COMMENT '任务执行过程ID',
  `task_id` int(11) NOT NULL COMMENT '主任务表id',
  `sub_task_id` int(11) DEFAULT NULL COMMENT '对应的子任务表ID',
  `completion_rate` int(11) DEFAULT NULL COMMENT '完成度',
  `completion_description` text COLLATE utf8_unicode_ci COMMENT '完成情况说明',
  `execution_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '当前时间',
  `submitter` int(11) NOT NULL COMMENT '提交人',
  `modify_by` int(11) NOT NULL COMMENT '修改人',
  `state` int(11) NOT NULL COMMENT '状态',
  `type` int(2) NOT NULL COMMENT 'l类型 属于主任务还子任务'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='任务执行过程表';

-- --------------------------------------------------------

--
-- 表的结构 `task_participants`
--

CREATE TABLE `task_participants` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL COMMENT '用户表id',
  `task_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='任务相关人表';

-- --------------------------------------------------------

--
-- 表的结构 `task_types`
--

CREATE TABLE `task_types` (
  `tc_id` int(11) NOT NULL COMMENT '任务类型ID',
  `tc_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '任务类型名称',
  `tc_feature` int(11) DEFAULT NULL COMMENT '任务类型特征'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='任务类型表';

--
-- 转存表中的数据 `task_types`
--

INSERT INTO `task_types` (`tc_id`, `tc_name`, `tc_feature`) VALUES
(1, '单次任务', 1),
(2, '长期日报任务', 2);

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `chinese_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `department_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`user_id`, `username`, `chinese_name`, `password`, `department_id`) VALUES
(1, 'zl', '张立', 'z888', 0),
(2, 'lsk', '李胜凯', 'l888', 0),
(3, 'dn', '丁宁', 'd888', 0),
(4, 'ghe', '郭焕儿', 'g888', 0),
(5, 'hjl', '黄金兰', 'h888', 0),
(6, 'lml', '林梦绿', 'l888', 0),
(7, 'lw', '龙正午', 'l888', 0),
(8, 'mzf', '梅志峰', 'm888', 0),
(9, 'xzh', '谢正航', 'x888', 0),
(10, 'ljh', '梁俊豪', 'l888', 0),
(11, 'pzc', '彭志潮', 'p888', 0),
(12, 'lxl', '刘鑫', 'l888', 0),
(13, 'zw', '曾振文', 'z888', 0),
(14, 'dh', '邓杭', 'd888', 0),
(15, 'hyl', '何倚玲', 'h888', 0),
(16, 'ht', '黄涛', 'h888', 0),
(17, 'ldg', '赖德根', 'l888', 0),
(18, 'llj', '赖龙精', 'l888', 0),
(19, 'lxle', '刘晓磊', 'l888', 0),
(20, 'wzl', '吴振霖', 'w888', 0),
(21, 'xbq', '向邦全', 'x888', 0),
(22, 'yf', '易飞', 'y888', 0),
(23, 'zzc', '张志诚', 'z888', 0),
(24, 'xy', '徐衍', 'x888', 0),
(25, 'bqs', '柏青松', 'b888', 0),
(26, 'cjb', '陈嘉彬', 'c888', 0),
(27, 'cyj', '陈业锦', 'y888', 0),
(28, 'czf', '陈镇烽', 'c888', 0),
(29, 'nzl', '牛子龙', 'n888', 0),
(30, 'zj', '郑进', 'z888', 0),
(31, 'qf', '瞿峰', 'q888', 0),
(32, 'ccq', '蔡楚翘', 'c888', 0),
(33, 'fhq', '方慧琼', 'f888', 0),
(34, 'jgl', '栗桂玲', 'l888', 0),
(35, 'xlj', '肖丽君', 'x888', 0),
(36, 'swx', '宋伟鑫', 's888', 0),
(37, 'ljg', '刘敬龚', 'l888', 0),
(38, 'gyh', '古永辉', 'g888', 0),
(39, 'oys', '欧月盛', 'o888', 0),
(40, 'qj', '曲佳', 'q888', 0),
(41, 'wlp', '韦丽朋', 'w888', 0),
(42, 'yw', '杨韦', 'y888', 0),
(43, 'lf', '李芬', 'l888', 0),
(44, 'kjf', '柯锦烽', 'k888', 0),
(45, 'sjy', '苏嘉盈', 's888', 0),
(46, 'yyx', '叶怡欣', 'y888', 0),
(47, 'zlq', '郑凌琦', 'z888', 0);

-- --------------------------------------------------------

--
-- 表的结构 `work_tasks`
--

CREATE TABLE `work_tasks` (
  `task_id` int(11) NOT NULL,
  `task_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '任务名称',
  `creation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `creator` int(11) DEFAULT NULL COMMENT '创建者',
  `task_status` int(11) DEFAULT NULL COMMENT '状态',
  `task_class` int(11) NOT NULL COMMENT '任务类型',
  `progree` int(11) NOT NULL COMMENT '完成度',
  `participant` text COLLATE utf8_unicode_ci NOT NULL COMMENT '参与者数组字符串',
  `plan_time` datetime NOT NULL COMMENT '计划完成时间',
  `task_readme` text COLLATE utf8_unicode_ci NOT NULL COMMENT '任务说明'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转储表的索引
--

--
-- 表的索引 `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`department_id`);

--
-- 表的索引 `department_members`
--
ALTER TABLE `department_members`
  ADD PRIMARY KEY (`member_id`),
  ADD KEY `department_id` (`department_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `department_user`
--
ALTER TABLE `department_user`
  ADD KEY `department_id` (`department_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `discussions`
--
ALTER TABLE `discussions`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `functions`
--
ALTER TABLE `functions`
  ADD PRIMARY KEY (`function_id`);

--
-- 表的索引 `function_members`
--
ALTER TABLE `function_members`
  ADD PRIMARY KEY (`member_id`),
  ADD KEY `function_id` (`function_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`log_id`);

--
-- 表的索引 `setp_progress`
--
ALTER TABLE `setp_progress`
  ADD PRIMARY KEY (`sp_id`);

--
-- 表的索引 `sub_tasks`
--
ALTER TABLE `sub_tasks`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `sub_task_step`
--
ALTER TABLE `sub_task_step`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `task_execution`
--
ALTER TABLE `task_execution`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `task_participants`
--
ALTER TABLE `task_participants`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `task_types`
--
ALTER TABLE `task_types`
  ADD PRIMARY KEY (`tc_id`);

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- 表的索引 `work_tasks`
--
ALTER TABLE `work_tasks`
  ADD PRIMARY KEY (`task_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `departments`
--
ALTER TABLE `departments`
  MODIFY `department_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- 使用表AUTO_INCREMENT `department_members`
--
ALTER TABLE `department_members`
  MODIFY `member_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- 使用表AUTO_INCREMENT `discussions`
--
ALTER TABLE `discussions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '讨论ID';

--
-- 使用表AUTO_INCREMENT `functions`
--
ALTER TABLE `functions`
  MODIFY `function_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- 使用表AUTO_INCREMENT `function_members`
--
ALTER TABLE `function_members`
  MODIFY `member_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- 使用表AUTO_INCREMENT `log`
--
ALTER TABLE `log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `setp_progress`
--
ALTER TABLE `setp_progress`
  MODIFY `sp_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `sub_tasks`
--
ALTER TABLE `sub_tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '子任务ID';

--
-- 使用表AUTO_INCREMENT `sub_task_step`
--
ALTER TABLE `sub_task_step`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `task_execution`
--
ALTER TABLE `task_execution`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '任务执行过程ID';

--
-- 使用表AUTO_INCREMENT `task_participants`
--
ALTER TABLE `task_participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `task_types`
--
ALTER TABLE `task_types`
  MODIFY `tc_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '任务类型ID', AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- 使用表AUTO_INCREMENT `work_tasks`
--
ALTER TABLE `work_tasks`
  MODIFY `task_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
