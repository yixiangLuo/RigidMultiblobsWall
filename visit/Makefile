# location of the Python header files
PYTHON_VERSION = 2.7
PYTHON_DIR = /home/yixiang/.conda/envs/py2
# PYTHON_DIR = /usr/local/pkg/python/$(PYTHON_VERSION)
PYTHON_INCLUDE = $(PYTHON_DIR)/include/python$(PYTHON_VERSION)
PYTHON_LIB = $(PYTHON_DIR)/lib/python$(PYTHON_VERSION)/config/

# location of the Boost Python include files and library
BOOST_INC = /usr/include/boost/
BOOST_LIB = /usr/lib/x86_64-linux-gnu/

# compile mesh classes
TARGET = visit_writer_interface

$(TARGET).so: $(TARGET).o
	g++ -shared  -dynamiclib $(TARGET).o -L$(BOOST_LIB)  -lboost_python -L$(PYTHON_LIB) -lpython$(PYTHON_VERSION) -o $(TARGET).so
	g++ -shared  -dynamiclib $(TARGET).o -L$(BOOST_LIB)  -lboost_python -L$(PYTHON_LIB) -lpython$(PYTHON_VERSION) -o $(TARGET).so

$(TARGET).o: $(TARGET).cc
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cc
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c visit_writer.c

clean: 
	rm -f $(TARGET).o $(TARGET).so
