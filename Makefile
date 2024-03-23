# Define filesystems to test
FILESYSTEMS = ext4 vfat nilfs2

# Define the workflow file
#WORKFLOW_FILE = workloads/filemicro_seqwrite.f
WORKFLOW_FILE = workloads/filemicro_createfiles.f

# Define the command to run Filebench
FILEBENCH_BIN = filebench/filebench
FILEBENCH_CMD = $(FILEBENCH_BIN) -f $(WORKFLOW_FILE)

# Path to mount the filesystem
MOUNT_PATH = /media/sdcard

# Block device to run on
BLOCK_DEVICE = /dev/mmcblk0p1

# Directory to store logs
LOG_DIR = logs

# Number of iterations
NITER = 1

# Define targets for each filesystem
.PHONY: all clean disable_randva $(FILESYSTEMS)

all: $(foreach i, $(FILESYSTEMS), $(LOG_DIR)/$(i).log)

ext4:
	mkfs.ext4 -F $(BLOCK_DEVICE)

vfat:
	mkfs.vfat $(BLOCK_DEVICE)

nilfs2:
	mkfs.nilfs2 -f $(BLOCK_DEVICE)

# disable random virtual address space for filebench to work
disable_randva:
	echo 0 > /proc/sys/kernel/randomize_va_space

$(LOG_DIR)/%.log: disable_randva %
	touch $@
	mount $(BLOCK_DEVICE) $(MOUNT_PATH)
	$(foreach i, $(shell seq 1 $(NITER)), $(FILEBENCH_CMD) > $@;)
	umount $(BLOCK_DEVICE)

clean:
	@echo "Cleaning up..."
	umount $(BLOCK_DEVICE)
	rm $(LOG_DIR)/*.log
	@echo "Done!"
