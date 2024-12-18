-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2024 at 10:22 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `greengrid`
--

-- --------------------------------------------------------

--
-- Table structure for table `agriculturalanalyst`
--

CREATE TABLE `agriculturalanalyst` (
  `AEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `agriculturaloffice`
--

CREATE TABLE `agriculturaloffice` (
  `AgriOfficeID` int(11) NOT NULL,
  `AgriOfficeName` varchar(50) NOT NULL,
  `Number` varchar(11) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Street` text NOT NULL,
  `City` text NOT NULL,
  `PostalCode` varchar(6) NOT NULL,
  `LocalGovtID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agriculturaloffice`
--

INSERT INTO `agriculturaloffice` (`AgriOfficeID`, `AgriOfficeName`, `Number`, `Email`, `Street`, `City`, `PostalCode`, `LocalGovtID`) VALUES
(12, 'Bangladesh Agricultural Research Institute', '01700000001', 'bari@bangladesh.gov.bd', 'Farmgate', 'Dhaka', '1000', 1),
(13, 'Department of Agriculture', '01700000002', 'doa@bangladesh.gov.bd', 'Agricultural Zone', 'Mymensingh', '2200', 2),
(14, 'Palli Karma-Sahayak Foundation', '01700000003', 'pksp@bangladesh.gov.bd', 'Agricultural Office Road', 'Chittagong', '4000', 3),
(15, 'Bangladesh Rural Development Board', '01700000004', 'brdb@bangladesh.gov.bd', 'Rajshahi Agro Center', 'Rajshahi', '6000', 4),
(16, 'Agricultural Marketing Directorate', '01700000005', 'amd@bangladesh.gov.bd', 'Agro Road', 'Khulna', '9000', 5);

-- --------------------------------------------------------

--
-- Table structure for table `agriculturalofficer`
--

CREATE TABLE `agriculturalofficer` (
  `OEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `demand`
--

CREATE TABLE `demand` (
  `ShopID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `RequestedQuantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dispatch`
--

CREATE TABLE `dispatch` (
  `DispatchID` int(11) NOT NULL,
  `WarehouseID` int(11) NOT NULL,
  `OrderID` int(11) NOT NULL,
  `DispatchDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dispatch`
--

INSERT INTO `dispatch` (`DispatchID`, `WarehouseID`, `OrderID`, `DispatchDate`) VALUES
(10, 19, 20, '2024-12-19'),
(11, 22, 24, '2024-12-19'),
(12, 22, 25, '2024-12-19'),
(13, 19, 26, '2024-12-19'),
(14, 19, 27, '2024-12-19'),
(15, 19, 28, '2024-12-19');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `EmployeeID` int(11) NOT NULL,
  `EmployeeName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `AgriOfficeID` int(11) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL,
  `EmployeeType` enum('O','A','W') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `FarmerID` int(11) NOT NULL,
  `FarmerName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farmer_deliver`
--

CREATE TABLE `farmer_deliver` (
  `FarmerID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `WarehouseID` int(11) NOT NULL,
  `ProductQuantity` decimal(10,2) NOT NULL,
  `PricePerUnit` decimal(10,2) NOT NULL,
  `DeliveryStatus` enum('Pending','In Transit','Delivered') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farmer_subsidery`
--

CREATE TABLE `farmer_subsidery` (
  `FarmerID` int(11) NOT NULL,
  `OEmployeeID` int(11) NOT NULL,
  `SubsideryQuantity` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farmer_subsidery_type`
--

CREATE TABLE `farmer_subsidery_type` (
  `FarmerID` int(11) NOT NULL,
  `OEmployeeID` int(11) NOT NULL,
  `SubsideryType` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `localgovernment`
--

CREATE TABLE `localgovernment` (
  `LocalGovtID` int(11) NOT NULL,
  `LocalGovtName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `localgovernment`
--

INSERT INTO `localgovernment` (`LocalGovtID`, `LocalGovtName`, `Number`, `Email`, `Street`, `City`, `PostalCode`) VALUES
(1, 'Dhaka City Corporation', '01721234567', 'dhakacc@bangladesh.gov.bd', 'Purana Paltan', 'Dhaka', '1000'),
(2, 'Mymensingh City Corporation', '01731234567', 'mymensinghcc@bangladesh.gov.bd', 'Mymensingh Sadar', 'Mymensingh', '2200'),
(3, 'Chittagong City Corporation', '01741234567', 'ctgcc@bangladesh.gov.bd', 'Karnaphuli', 'Chittagong', '4000'),
(4, 'Rajshahi City Corporation', '01751234567', 'rajshahicc@bangladesh.gov.bd', 'Rajshahi Sadar', 'Rajshahi', '6000'),
(5, 'Khulna City Corporation', '01761234567', 'khulnacc@bangladesh.gov.bd', 'Khulna Sadar', 'Khulna', '9000');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `OrderID` int(11) NOT NULL,
  `OrderDate` date NOT NULL,
  `OrderStatus` enum('Pending','Accepted','Delivered','Cancelled') NOT NULL,
  `ShopID` int(11) NOT NULL,
  `WarehouseID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`OrderID`, `OrderDate`, `OrderStatus`, `ShopID`, `WarehouseID`) VALUES
(20, '2024-12-19', 'Delivered', 18, 19),
(24, '2024-12-19', 'Delivered', 18, 22),
(25, '2024-12-19', 'Delivered', 17, 22),
(26, '2024-12-19', 'Delivered', 18, 19),
(27, '2024-12-19', 'Delivered', 17, 19),
(28, '2024-12-19', 'Delivered', 18, 19);

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--

CREATE TABLE `order_details` (
  `OrderID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `OrderQuantity` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_details`
--

INSERT INTO `order_details` (`OrderID`, `ProductID`, `OrderQuantity`) VALUES
(20, 17, '100'),
(24, 21, '10000'),
(25, 22, '100'),
(26, 22, '10'),
(27, 22, '20'),
(28, 22, '100');

-- --------------------------------------------------------

--
-- Table structure for table `price_history`
--

CREATE TABLE `price_history` (
  `PriceHistoryID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `PricePerUnit` decimal(10,2) NOT NULL,
  `UpdatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `ProductID` int(11) NOT NULL,
  `ProductName` varchar(100) NOT NULL,
  `Category` varchar(100) NOT NULL,
  `PricePerUnit` varchar(255) NOT NULL,
  `Seasonality` varchar(50) NOT NULL,
  `Unit` varchar(255) NOT NULL,
  `OEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`ProductID`, `ProductName`, `Category`, `PricePerUnit`, `Seasonality`, `Unit`, `OEmployeeID`) VALUES
(17, 'Potato', 'Vegetables', '7', 'All Year', 'Kilogram', 33),
(21, 'Rice', 'Grains', '105', 'All Year', 'Gram (g)', 33),
(22, 'Apples', 'Fruits', '49', 'Spring', 'Dozen', 33);

-- --------------------------------------------------------

--
-- Table structure for table `productiondata`
--

CREATE TABLE `productiondata` (
  `ProductionID` int(11) NOT NULL,
  `HarvestDate` date NOT NULL,
  `ProductionCost` decimal(10,2) NOT NULL,
  `Acreage` decimal(10,2) DEFAULT NULL,
  `YieldAmount` decimal(10,2) DEFAULT NULL,
  `FarmerID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `YieldUnit` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `productiondata`
--

INSERT INTO `productiondata` (`ProductionID`, `HarvestDate`, `ProductionCost`, `Acreage`, `YieldAmount`, `FarmerID`, `ProductID`, `YieldUnit`) VALUES
(9, '2024-12-18', 20000.00, 1.00, 100.00, 54, 17, 'kg');

-- --------------------------------------------------------

--
-- Table structure for table `retailshop`
--

CREATE TABLE `retailshop` (
  `ShopID` int(11) NOT NULL,
  `ShopName` varchar(50) NOT NULL,
  `Number` varchar(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Street` text DEFAULT NULL,
  `City` text DEFAULT NULL,
  `PostalCode` varchar(6) DEFAULT NULL,
  `OwnerID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `retailshop`
--

INSERT INTO `retailshop` (`ShopID`, `ShopName`, `Number`, `Email`, `Street`, `City`, `PostalCode`, `OwnerID`) VALUES
(17, 'Agora', '1234567888', 'agora2@gmail.com', 'Dhanmondi 27', 'Dhaka', '123456', 59),
(18, 'Meena Baazar', '1234567678', 'meena@gmail.com', 'Dhanmondi 9', 'Dhaka', '123456', 65);

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

CREATE TABLE `stock` (
  `StockID` int(11) NOT NULL,
  `StockQuantity` decimal(10,2) DEFAULT NULL,
  `LastUpdateDate` date DEFAULT NULL,
  `StockAvailability` enum('Incoming','Outgoing') DEFAULT NULL,
  `WarehouseID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock`
--

INSERT INTO `stock` (`StockID`, `StockQuantity`, `LastUpdateDate`, `StockAvailability`, `WarehouseID`, `ProductID`) VALUES
(35, 1000.00, '2024-12-19', 'Incoming', 19, 17),
(39, 100.00, '2024-12-19', 'Outgoing', 19, 17),
(41, 20000.00, '2024-12-19', 'Incoming', 22, 21),
(42, 10000.00, '2024-12-19', 'Outgoing', 22, 21),
(43, 1000.00, '2024-12-19', 'Incoming', 22, 22),
(44, 1000.00, '2024-12-19', 'Incoming', 22, 17),
(45, 100.00, '2024-12-19', 'Outgoing', 22, 22),
(46, 10000.00, '2024-12-19', 'Incoming', 19, 22),
(47, 10.00, '2024-12-19', 'Outgoing', 19, 22),
(48, 20.00, '2024-12-19', 'Outgoing', 19, 22),
(49, 100.00, '2024-12-19', 'Outgoing', 19, 22);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `PasswordHash` varchar(255) DEFAULT NULL,
  `Role` enum('O','A','W','S','F') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `FirstName`, `LastName`, `Username`, `Email`, `PasswordHash`, `Role`) VALUES
(1, 'Mymuna', 'Rahman', 'admin', 'admin@gmail.com', 'pbkdf2:sha256:1000000$0i7lmoUwPxQZnkmZ$8660e6cac662e99ffdc638f199abfe552c6d83b0821281e0382f74197ae086a9', ''),
(29, 'Mahmud', 'Hasan', 'mahmud33', 'mahmud@gmail.com', 'pbkdf2:sha256:1000000$pfU5SVhP1R0e8ewh$a43203302fb6c930ee6e2f8d384acde86e1d5ac0990e2162b0a425f296d1186c', 'A'),
(33, 'Tanvir', 'Rahman', 'tanvir33', 'tanvir@gmail.com', 'pbkdf2:sha256:1000000$lsBxjfcNhKbKFXjT$c4c072c05dedc3f00874f5d942954f16356a085f0d2b7e214d40789bc94121a6', 'O'),
(48, 'Roni', 'Alam', 'roni34', 'roni@gmail.com', 'pbkdf2:sha256:1000000$TsClBAbSxcY8X0Lh$aee178445d9c7ca2f8d3a094dcc4df5b9bcbcd24e55d98898b7193a8025c9137', 'A'),
(50, 'Samia', 'Saba', 'samia33', 'samia@gmail.com', 'pbkdf2:sha256:1000000$TZRYPvKoUgP7mvWc$1aa2501e1e719f4f01a2c3e95e894f38a8b76462744947fce8213fb211420d91', 'W'),
(54, 'Kafi', 'asd', 'kafi33', 'kafi@gmail.com', 'pbkdf2:sha256:1000000$7FOTCSVt9kZxu75g$88256fc6a63bc26e86b8acb15a8fe24512cd6365c17a881838a0d809c2cde24a', 'F'),
(57, 'Ibrahim', 'Hasan', 'ibrahim33', 'ibrahim@gmail.com', 'pbkdf2:sha256:1000000$34o5T2gCOrSytATI$7d3cc1c1cd39720a57bf9ceb756895332120612b556294f900f0af4e16ef7458', 'O'),
(59, 'Tasnia', 'Khan', 'tasnia33', 'tasniakhan@gmail.com', 'pbkdf2:sha256:1000000$vLtE7el1CljZmAfk$890cc79cc666b02753942e66bd6eb14be2d281ce7b98e8df5d4aa9d5a181abbd', 'S'),
(64, 'Aisha', 'Rahman', 'aisha33', 'aisha@gmail.com', 'pbkdf2:sha256:1000000$IAnHxlzOzqPsdVrC$3015a34eeb3e823b1bb619726419460599003eff201fbb5261455bf92ef5a5fc', 'F'),
(65, 'Fariha', 'Mirza', 'mirza33', 'mirza@gmail.com', 'pbkdf2:sha256:1000000$69h8NBrGXTYlhuLo$e405e3d42874ae476a492920fdc5227f524aa7e1ddcf0093ec6079a2c26a3ab7', 'S'),
(66, 'Opu', 'Chowdhury', 'opu33', 'opu@gmail.com', 'pbkdf2:sha256:1000000$yXZCG87xvXZcBgJh$1909190095fb4b5b8a0dc38abc6c5b2ca90592afacf928c02d1ca315f96cddf7', 'W');

-- --------------------------------------------------------

--
-- Table structure for table `warehouse`
--

CREATE TABLE `warehouse` (
  `WarehouseID` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Street` text NOT NULL,
  `City` text NOT NULL,
  `PostalCode` varchar(6) NOT NULL,
  `Temperature` decimal(5,2) NOT NULL,
  `Humidity` decimal(5,2) NOT NULL,
  `LightExposure` decimal(6,2) NOT NULL,
  `WEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehouse`
--

INSERT INTO `warehouse` (`WarehouseID`, `Name`, `Street`, `City`, `PostalCode`, `Temperature`, `Humidity`, `LightExposure`, `WEmployeeID`) VALUES
(19, 'Bashundhara R/A Warehouse', 'Bashundhara Block K', 'Dhaka', '123445', 22.00, 22.00, 22.00, 50),
(22, 'Mirpur-Warehouse A', 'Mirupur 10', 'Dhaka', '123457', 44.00, 44.00, 44.00, 66);

-- --------------------------------------------------------

--
-- Table structure for table `warehousemanager`
--

CREATE TABLE `warehousemanager` (
  `WEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agriculturalanalyst`
--
ALTER TABLE `agriculturalanalyst`
  ADD PRIMARY KEY (`AEmployeeID`);

--
-- Indexes for table `agriculturaloffice`
--
ALTER TABLE `agriculturaloffice`
  ADD PRIMARY KEY (`AgriOfficeID`),
  ADD UNIQUE KEY `number` (`Number`),
  ADD UNIQUE KEY `email` (`Email`),
  ADD KEY `FK_AgriOffice_LocalGov` (`LocalGovtID`);

--
-- Indexes for table `agriculturalofficer`
--
ALTER TABLE `agriculturalofficer`
  ADD PRIMARY KEY (`OEmployeeID`);

--
-- Indexes for table `demand`
--
ALTER TABLE `demand`
  ADD PRIMARY KEY (`ShopID`,`ProductID`),
  ADD KEY `demand_ibfk_2` (`ProductID`);

--
-- Indexes for table `dispatch`
--
ALTER TABLE `dispatch`
  ADD PRIMARY KEY (`DispatchID`),
  ADD KEY `WarehouseID` (`WarehouseID`),
  ADD KEY `OrderID` (`OrderID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`EmployeeID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `FK_Employee_Government` (`AgriOfficeID`);

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`FarmerID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `farmer_deliver`
--
ALTER TABLE `farmer_deliver`
  ADD PRIMARY KEY (`FarmerID`,`ProductID`,`WarehouseID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `WarehouseID` (`WarehouseID`);

--
-- Indexes for table `farmer_subsidery`
--
ALTER TABLE `farmer_subsidery`
  ADD PRIMARY KEY (`FarmerID`,`OEmployeeID`),
  ADD KEY `FK2_farmer_subsidery` (`OEmployeeID`);

--
-- Indexes for table `farmer_subsidery_type`
--
ALTER TABLE `farmer_subsidery_type`
  ADD PRIMARY KEY (`FarmerID`,`OEmployeeID`,`SubsideryType`);

--
-- Indexes for table `localgovernment`
--
ALTER TABLE `localgovernment`
  ADD PRIMARY KEY (`LocalGovtID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD UNIQUE KEY `unique_Number` (`Number`),
  ADD UNIQUE KEY `unique_Email` (`Email`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `ShopID` (`ShopID`),
  ADD KEY `order_warehouse_id` (`WarehouseID`);

--
-- Indexes for table `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`OrderID`,`ProductID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `price_history`
--
ALTER TABLE `price_history`
  ADD PRIMARY KEY (`PriceHistoryID`),
  ADD KEY `FK_price_history_product` (`ProductID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `officer_user_FK1` (`OEmployeeID`);

--
-- Indexes for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD PRIMARY KEY (`ProductionID`),
  ADD KEY `FarmerID` (`FarmerID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `retailshop`
--
ALTER TABLE `retailshop`
  ADD PRIMARY KEY (`ShopID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `OwnerID` (`OwnerID`);

--
-- Indexes for table `stock`
--
ALTER TABLE `stock`
  ADD PRIMARY KEY (`StockID`),
  ADD KEY `stock_ibfk_1` (`WarehouseID`),
  ADD KEY `stock_ibfk_2` (`ProductID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `username` (`Username`),
  ADD UNIQUE KEY `email` (`Email`);

--
-- Indexes for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD PRIMARY KEY (`WarehouseID`),
  ADD KEY `WEmployeeID` (`WEmployeeID`);

--
-- Indexes for table `warehousemanager`
--
ALTER TABLE `warehousemanager`
  ADD PRIMARY KEY (`WEmployeeID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agriculturaloffice`
--
ALTER TABLE `agriculturaloffice`
  MODIFY `AgriOfficeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `dispatch`
--
ALTER TABLE `dispatch`
  MODIFY `DispatchID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `EmployeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `FarmerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `localgovernment`
--
ALTER TABLE `localgovernment`
  MODIFY `LocalGovtID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `price_history`
--
ALTER TABLE `price_history`
  MODIFY `PriceHistoryID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `productiondata`
--
ALTER TABLE `productiondata`
  MODIFY `ProductionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `retailshop`
--
ALTER TABLE `retailshop`
  MODIFY `ShopID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `stock`
--
ALTER TABLE `stock`
  MODIFY `StockID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `warehouse`
--
ALTER TABLE `warehouse`
  MODIFY `WarehouseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agriculturalanalyst`
--
ALTER TABLE `agriculturalanalyst`
  ADD CONSTRAINT `FK_AgriculturalAnalyst_Employee` FOREIGN KEY (`AEmployeeID`) REFERENCES `employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `agriculturaloffice`
--
ALTER TABLE `agriculturaloffice`
  ADD CONSTRAINT `FK_AgriOffice_LocalGov` FOREIGN KEY (`LocalGovtID`) REFERENCES `localgovernment` (`LocalGovtID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `agriculturalofficer`
--
ALTER TABLE `agriculturalofficer`
  ADD CONSTRAINT `FK_OEmployeeID_Employee` FOREIGN KEY (`OEmployeeID`) REFERENCES `employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `demand`
--
ALTER TABLE `demand`
  ADD CONSTRAINT `demand_ibfk_1` FOREIGN KEY (`ShopID`) REFERENCES `retailshop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `demand_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `dispatch`
--
ALTER TABLE `dispatch`
  ADD CONSTRAINT `dispatch_ibfk_1` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `dispatch_ibfk_2` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `FK_Employee_AgriOffice` FOREIGN KEY (`AgriOfficeID`) REFERENCES `agriculturaloffice` (`AgriOfficeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `farmer_deliver`
--
ALTER TABLE `farmer_deliver`
  ADD CONSTRAINT `farmer_deliver_ibfk_1` FOREIGN KEY (`FarmerID`) REFERENCES `farmer` (`FarmerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `farmer_deliver_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `farmer_deliver_ibfk_3` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `farmer_subsidery`
--
ALTER TABLE `farmer_subsidery`
  ADD CONSTRAINT `FK1_farmer_subsidery` FOREIGN KEY (`FarmerID`) REFERENCES `farmer` (`FarmerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK2_farmer_subsidery` FOREIGN KEY (`OEmployeeID`) REFERENCES `agriculturalofficer` (`OEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `farmer_subsidery_type`
--
ALTER TABLE `farmer_subsidery_type`
  ADD CONSTRAINT `farmer_subsidery_type_ibfk_1` FOREIGN KEY (`FarmerID`,`OEmployeeID`) REFERENCES `farmer_subsidery` (`FarmerID`, `OEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`ShopID`) REFERENCES `retailshop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_warehouse_id` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `price_history`
--
ALTER TABLE `price_history`
  ADD CONSTRAINT `FK_price_history_product` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `officer_user_FK1` FOREIGN KEY (`OEmployeeID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD CONSTRAINT `productiondata_farmer_fk` FOREIGN KEY (`FarmerID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_3` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `retailshop`
--
ALTER TABLE `retailshop`
  ADD CONSTRAINT `retailshop_ibfk_1` FOREIGN KEY (`OwnerID`) REFERENCES `users` (`UserID`);

--
-- Constraints for table `stock`
--
ALTER TABLE `stock`
  ADD CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD CONSTRAINT `warehouse_ibfk_1` FOREIGN KEY (`WEmployeeID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warehousemanager`
--
ALTER TABLE `warehousemanager`
  ADD CONSTRAINT `FK_WarehouseManager_Employee` FOREIGN KEY (`WEmployeeID`) REFERENCES `employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
