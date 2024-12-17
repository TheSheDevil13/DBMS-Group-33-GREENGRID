-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 17, 2024 at 08:20 PM
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
(3, 16, 12, '2024-11-01'),
(4, 16, 13, '2024-12-10'),
(5, 16, 14, '2024-12-10'),
(6, 16, 15, '2024-12-10'),
(7, 16, 16, '2024-12-10');

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

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`FarmerID`, `FarmerName`, `Number`, `Email`, `Street`, `City`, `PostalCode`) VALUES
(1, 'Abdul Karim', '01711223345', 'karim@farmer.com', 'Dhanmondi, Dhaka', 'Dhaka', '1209'),
(2, 'Fatema Akter', '01722334456', 'fatema@farmer.com', 'Madhupur, Tangail', 'Tangail', '1900'),
(3, 'Hasan Ali', '01733445567', 'hasan@farmer.com', 'Narsingdi, Dhaka', 'Narsingdi', '1600'),
(4, 'Shamim Hossain', '01744556678', 'shamim@farmer.com', 'Feni, Chittagong', 'Feni', '3900'),
(5, 'Salma Begum', '01755667789', 'salma@farmer.com', 'Chandpur, Chittagong', 'Chandpur', '4200');

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
(12, '2024-12-10', 'Delivered', 5, 16),
(13, '2024-12-10', 'Delivered', 7, 16),
(14, '2024-12-10', 'Delivered', 4, 16),
(15, '2024-12-10', 'Delivered', 4, 16),
(16, '2024-12-10', 'Delivered', 3, 16),
(17, '2024-12-10', 'Accepted', 5, 16);

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
(12, 11, '500'),
(12, 12, '50'),
(13, 12, '50'),
(14, 11, '100'),
(15, 11, '100'),
(16, 11, '200'),
(17, 13, '1200');

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
  `Unit` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`ProductID`, `ProductName`, `Category`, `PricePerUnit`, `Seasonality`, `Unit`) VALUES
(11, 'Freya Huber', 'Vegetables', '644', 'Summer', 'Kilogram (kg)'),
(12, 'Inga Butler', 'Meat', '758', 'All Year', 'Dozen'),
(13, 'Audra Bradshaw', 'Meat', '499', 'Winter', 'Pieces (pcs)'),
(14, 'Sarah Martinez', 'Others', '599', 'Autumn', 'Liter (l)'),
(15, 'Potatoes', 'Vegetables', '13', 'All Year', 'Kilogram (kg)');

-- --------------------------------------------------------

--
-- Table structure for table `productiondata`
--

CREATE TABLE `productiondata` (
  `ProductionID` int(11) NOT NULL,
  `HarvestDate` date NOT NULL,
  `ProductionCost` decimal(10,2) NOT NULL,
  `ShelfLife` varchar(50) DEFAULT NULL,
  `Acreage` decimal(10,2) DEFAULT NULL,
  `YieldRate` decimal(10,2) DEFAULT NULL,
  `AEmployeeID` int(11) NOT NULL,
  `FarmerID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `PostalCode` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `retailshop`
--

INSERT INTO `retailshop` (`ShopID`, `ShopName`, `Number`, `Email`, `Street`, `City`, `PostalCode`) VALUES
(2, 'Unimart', '01800987654', 'unimart@example.com', 'House 12, Street 5', 'Chittagong', '4203'),
(3, 'Meena Bazar', '01800223344', 'meena@example.com', 'Block A, Shyamoli', 'Rajshahi', '6201'),
(4, 'Gulshan Market', '01800334455', 'gulshan@example.com', 'House 5, Road 3', 'Dhaka', '1212'),
(5, 'Agora', '01800445566', 'agora@example.com', 'Plot 3, Main Road', 'Sylhet', '3100'),
(6, 'Lyle Hicks', '01773301138', 'radity@mailinator.com', 'Illum molestiae per', 'Culpa consequatur es', '5681'),
(7, 'Guinevere Weiss', '01773301139', 'jinyhum@mailinator.com', 'Omnis sequi proident', 'Veniam cum consecte', '7830');

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
(17, 500.00, '2024-12-10', 'Incoming', 16, 11),
(18, 500.00, '2024-12-10', 'Incoming', 16, 11),
(19, 100.00, '2024-12-09', 'Incoming', 16, 12),
(20, 100.00, '2024-12-08', 'Incoming', 16, 12),
(21, 1000.00, '2024-12-07', 'Outgoing', 16, 11),
(22, 50.00, '2024-12-06', 'Outgoing', 16, 12),
(23, 150.00, '2024-12-05', 'Outgoing', 16, 12),
(24, 500.00, '2024-12-04', 'Incoming', 16, 11),
(25, 100.00, '2024-12-03', 'Outgoing', 16, 11),
(26, 100.00, '2024-12-02', 'Outgoing', 16, 11),
(27, 5000.00, '2024-12-01', 'Incoming', 16, 14),
(28, 800.00, '2024-12-10', 'Incoming', 16, 11),
(29, 200.00, '2024-12-10', 'Outgoing', 16, 11),
(31, 900.00, '2024-12-18', 'Incoming', 16, 12);

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
(28, 'Ariful', 'Islam', 'ariful33', 'ariful@gmail.com', 'pbkdf2:sha256:1000000$ZCFDi3tZCCa62wbG$1e97008b1e06d7169aa2d2625f2ad5ebb3c885c4270f6ba2117bd861becaa6e0', 'O'),
(29, 'Mahmud', 'Hasan', 'mahmud33', 'mahmud@gmail.com', 'pbkdf2:sha256:1000000$pfU5SVhP1R0e8ewh$a43203302fb6c930ee6e2f8d384acde86e1d5ac0990e2162b0a425f296d1186c', 'A'),
(30, 'Nadia', 'Sultana', 'nadia33', 'nadia@gmail.com', 'pbkdf2:sha256:1000000$jo106inzd9S0GhlQ$b1cd331026d57f33b826b4783f0b2a4f53cbffd5daa7cb46b99d9ed4ca47ab1c', 'W'),
(33, 'Tanvir', 'Rahman', 'tanvir33', 'tanvir@gmail.com', 'pbkdf2:sha256:1000000$lsBxjfcNhKbKFXjT$c4c072c05dedc3f00874f5d942954f16356a085f0d2b7e214d40789bc94121a6', 'O'),
(47, 'Mymuna', 'Rahman', 'mymxnaaaaa', 'theshedevil14@gmail.com', 'pbkdf2:sha256:1000000$6ginJKsPUn2TB4rK$303a513020ccf527945a291af88a9e9d289f3a2ab825435b0b6a826b038b63e6', 'O'),
(48, 'Roni', 'Alam', 'roni33', 'roni@gmail.com', 'pbkdf2:sha256:1000000$TsClBAbSxcY8X0Lh$aee178445d9c7ca2f8d3a094dcc4df5b9bcbcd24e55d98898b7193a8025c9137', 'A'),
(49, 'sdc', 'Rahman', 'mymxnaadd', 'mymunarahman03@gmail.comdd', 'pbkdf2:sha256:1000000$rc1N2GJjtDc54NLe$e98298fa8af668d79ff887fc674e30734fbf090aa7bd7f6f2ea2908152ba3a36', 'A'),
(50, 'Samia', 'Saba', 'samia33', 'samia@gmail.com', 'pbkdf2:sha256:1000000$TZRYPvKoUgP7mvWc$1aa2501e1e719f4f01a2c3e95e894f38a8b76462744947fce8213fb211420d91', 'W'),
(51, 'Test', 'a', 'test', 'warehouse@gmail.com', 'pbkdf2:sha256:1000000$5IrzKFPAFAwo61tm$a18edb8c18863a6e807d886f375153abc27cfc9fd75807aceeb27242b37e16eb', 'W'),
(52, 'Lars', 'Randolph', 'suhopava', 'pedeq@mailinator.com', 'pbkdf2:sha256:1000000$JQjUYj0HjD3CJrTu$033a9fddaf60a942968766f030d811419d8e1d32bbddee203c5f079c05dd78b3', 'W'),
(53, 'Russell', 'Schultz', 'jygygituxa', 'pedys@mailinator.com', 'pbkdf2:sha256:1000000$JlJnyrD3ZwI4u9Hz$2dfd22ab0243bb09046efdb2422c99c83c0c9547b08e77be28c85b16f7738496', 'W'),
(54, 'Kafi', 'asd', 'kafi33', 'kafi@gmail.com', 'pbkdf2:sha256:1000000$7FOTCSVt9kZxu75g$88256fc6a63bc26e86b8acb15a8fe24512cd6365c17a881838a0d809c2cde24a', 'F'),
(55, 'Khan', 'Asad', 'unimart', 'unimart@gmail.com', 'pbkdf2:sha256:1000000$XW2CbyLqRc3mgmnw$78c1aac700e0c585be4e9a2144fe06b61afcca1fe080889b1ad0ac8069afc92b', 'S');

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
(16, 'Dhaka - 1', 'Block: C, Road 113/W', 'Mirpur Cantonment', '5260', 978.00, 10.00, 48.00, 52),
(17, 'Nicholas Burnett', 'Temporibus tempor la', 'Occaecat elit paria', 'Vel ni', 949.00, 89.00, 7664.00, 51),
(19, 'asdfgh', '', '', '', 22.00, 22.00, 22.00, 50);

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
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`ProductID`);

--
-- Indexes for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD PRIMARY KEY (`ProductionID`),
  ADD KEY `AEmployeeID` (`AEmployeeID`),
  ADD KEY `FarmerID` (`FarmerID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `retailshop`
--
ALTER TABLE `retailshop`
  ADD PRIMARY KEY (`ShopID`),
  ADD UNIQUE KEY `Number` (`Number`),
  ADD UNIQUE KEY `Email` (`Email`);

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
  MODIFY `DispatchID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

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
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `productiondata`
--
ALTER TABLE `productiondata`
  MODIFY `ProductionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `retailshop`
--
ALTER TABLE `retailshop`
  MODIFY `ShopID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `stock`
--
ALTER TABLE `stock`
  MODIFY `StockID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `warehouse`
--
ALTER TABLE `warehouse`
  MODIFY `WarehouseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
-- Constraints for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD CONSTRAINT `productiondata_farmer_fk` FOREIGN KEY (`FarmerID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_1` FOREIGN KEY (`AEmployeeID`) REFERENCES `agriculturalanalyst` (`AEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_3` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

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
