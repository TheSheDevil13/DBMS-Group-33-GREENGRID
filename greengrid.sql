-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 27, 2024 at 06:15 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

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

--
-- Dumping data for table `agriculturalanalyst`
--

INSERT INTO `agriculturalanalyst` (`AEmployeeID`) VALUES
(10);

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

-- --------------------------------------------------------

--
-- Table structure for table `AgriculturalOfficer`
--

CREATE TABLE `AgriculturalOfficer` (
  `OEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `AgriculturalOfficer`
--

INSERT INTO `AgriculturalOfficer` (`OEmployeeID`) VALUES
(11);

-- --------------------------------------------------------

--
-- Table structure for table `Demand`
--

CREATE TABLE `Demand` (
  `ShopID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `RequestedQuantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Dispatch`
--

CREATE TABLE `Dispatch` (
  `WarehouseID` int(11) NOT NULL,
  `StockID` int(11) NOT NULL,
  `ShopID` int(11) NOT NULL,
  `DispatchQuantity` decimal(10,2) DEFAULT NULL,
  `DispatchDate` date DEFAULT NULL,
  `DispatchStatus` enum('Pending','In Transit','Delivered','Cancelled','Ready for Pickup') DEFAULT NULL,
  `DeliveryStatus` enum('Pending','In Transit','Delivered') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`EmployeeID`, `EmployeeName`, `Number`, `Email`, `AgriOfficeID`, `Street`, `City`, `PostalCode`, `EmployeeType`) VALUES
(10, 'John Doe', '01234567891', 'doe@gmail.com', NULL, NULL, NULL, NULL, 'O'),
(11, 'Jane Smith', '02099333791', 'smith@gmail.com', NULL, NULL, NULL, NULL, 'A'),
(12, 'Jane Smith', '07099333771', 'smith2@gmail.com', NULL, NULL, NULL, NULL, 'W');

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
(1, 'John Doe', '01234567891', 'doe@gmail.com', NULL, NULL, NULL),
(2, 'Jane Smith', '01099333791', 'smith@gmail.com', NULL, NULL, NULL);

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
(1, 'Union Agricultural Development Council', '01712345678', 'uadc@example.com', '123 Main Road', 'Dhaka', '1212'),
(2, 'District Agriculture Office', '01823456789', 'dao@example.com', '45 Green Street', 'Chittagong', '4220'),
(3, 'Upazila Agro-Resource Center', '01934567890', 'uarc@example.com', '78 Agrarian Avenue', 'Sylhet', '3100'),
(4, 'Rural Development Office', '01645678901', 'rdo@example.com', '50 Community Lane', 'Khulna', '9100'),
(5, 'Urban Agro Support Center', '01556789012', 'uasc@example.com', '99 City Park Blvd', 'Rajshahi', '6200');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `OrderID` int(11) NOT NULL,
  `OrderDate` date NOT NULL,
  `OrderStatus` enum('Pending','Processing','Shipped','Delivered','Cancelled','Returned') NOT NULL,
  `ShopID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--

CREATE TABLE `order_details` (
  `OrderID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `OrderQuantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `ProductID` int(11) NOT NULL,
  `OEmployeeID` int(11) NOT NULL,
  `ProductName` varchar(100) NOT NULL,
  `Category` varchar(100) NOT NULL,
  `PricePerUnit` decimal(10,2) NOT NULL,
  `Seasonality` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, 'Unimart', '123', 'unimart@gmail.com', NULL, NULL, NULL),
(2, 'Meena Bazaar', '1232', 'meenat@gmail.com', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `Stock`
--

CREATE TABLE `Stock` (
  `StockID` int(11) NOT NULL,
  `StockQuantity` decimal(10,2) DEFAULT NULL,
  `LastUpdateDate` date DEFAULT NULL,
  `StockAvailability` enum('In Stock','Out of Stock') DEFAULT NULL,
  `WarehouseID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warehouse`
--

CREATE TABLE `warehouse` (
  `WarehouseID` int(11) NOT NULL,
  `Street` text NOT NULL,
  `City` text NOT NULL,
  `PostalCode` varchar(6) NOT NULL,
  `Temperature` decimal(5,2) NOT NULL,
  `Humidity` decimal(5,2) NOT NULL,
  `LightExposure` decimal(6,2) NOT NULL,
  `WEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warehousemanager`
--

CREATE TABLE `warehousemanager` (
  `WEmployeeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehousemanager`
--

INSERT INTO `warehousemanager` (`WEmployeeID`) VALUES
(12);

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
-- Indexes for table `AgriculturalOfficer`
--
ALTER TABLE `AgriculturalOfficer`
  ADD PRIMARY KEY (`OEmployeeID`);

--
-- Indexes for table `Demand`
--
ALTER TABLE `Demand`
  ADD PRIMARY KEY (`ShopID`,`ProductID`),
  ADD KEY `demand_ibfk_2` (`ProductID`);

--
-- Indexes for table `Dispatch`
--
ALTER TABLE `Dispatch`
  ADD PRIMARY KEY (`WarehouseID`,`StockID`,`ShopID`),
  ADD KEY `dispatch_ibfk_2` (`StockID`),
  ADD KEY `dispatch_ibfk_3` (`ShopID`);

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
  ADD KEY `ShopID` (`ShopID`);

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
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `FK_Product_AgriOfficer` (`OEmployeeID`);

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
-- Indexes for table `Stock`
--
ALTER TABLE `Stock`
  ADD PRIMARY KEY (`StockID`),
  ADD KEY `stock_ibfk_1` (`WarehouseID`),
  ADD KEY `stock_ibfk_2` (`ProductID`);

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
  MODIFY `AgriOfficeID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `EmployeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `FarmerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `localgovernment`
--
ALTER TABLE `localgovernment`
  MODIFY `LocalGovtID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `productiondata`
--
ALTER TABLE `productiondata`
  MODIFY `ProductionID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `retailshop`
--
ALTER TABLE `retailshop`
  MODIFY `ShopID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Stock`
--
ALTER TABLE `Stock`
  MODIFY `StockID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `warehouse`
--
ALTER TABLE `warehouse`
  MODIFY `WarehouseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

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
-- Constraints for table `AgriculturalOfficer`
--
ALTER TABLE `AgriculturalOfficer`
  ADD CONSTRAINT `FK_OEmployeeID_Employee` FOREIGN KEY (`OEmployeeID`) REFERENCES `Employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Demand`
--
ALTER TABLE `Demand`
  ADD CONSTRAINT `demand_ibfk_1` FOREIGN KEY (`ShopID`) REFERENCES `RetailShop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `demand_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Dispatch`
--
ALTER TABLE `Dispatch`
  ADD CONSTRAINT `dispatch_ibfk_1` FOREIGN KEY (`WarehouseID`) REFERENCES `Warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `dispatch_ibfk_2` FOREIGN KEY (`StockID`) REFERENCES `Stock` (`StockID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `dispatch_ibfk_3` FOREIGN KEY (`ShopID`) REFERENCES `RetailShop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE;

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
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`ShopID`) REFERENCES `retailshop` (`ShopID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `FK_Product_AgriOfficer` FOREIGN KEY (`OEmployeeID`) REFERENCES `AgriculturalOfficer` (`OEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `productiondata`
--
ALTER TABLE `productiondata`
  ADD CONSTRAINT `productiondata_ibfk_1` FOREIGN KEY (`AEmployeeID`) REFERENCES `agriculturalanalyst` (`AEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_2` FOREIGN KEY (`FarmerID`) REFERENCES `farmer` (`FarmerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `productiondata_ibfk_3` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Stock`
--
ALTER TABLE `Stock`
  ADD CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`WarehouseID`) REFERENCES `Warehouse` (`WarehouseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD CONSTRAINT `warehouse_ibfk_1` FOREIGN KEY (`WEmployeeID`) REFERENCES `warehousemanager` (`WEmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warehousemanager`
--
ALTER TABLE `warehousemanager`
  ADD CONSTRAINT `FK_WarehouseManager_Employee` FOREIGN KEY (`WEmployeeID`) REFERENCES `employee` (`EmployeeID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
